from django.test import TestCase, override_settings, RequestFactory
from django.template import Template, Context
from django.urls import path, reverse
from django.http import HttpResponse

from .models import Menu, MenuItem
from ..menu_system.urls import urlpatterns


# Define dummy views and URL patterns for named URL testing

def dummy_view(request):
    return HttpResponse('OK')

urlpatterns=[
    path('', dummy_view, name='home'),
    path('about/', dummy_view, name='about'),
    path('services/', dummy_view, name='services'),
]

@override_settings(ROOT_URLCONF=__name__)
class DrawMenuTagTests(TestCase):
    def setUp(self):
        # Create main menu and items
        self.menu = Menu.objects.create(name='main')
        # Root items
        self.home_item = MenuItem.objects.create(
            menu=self.menu, name='Home', url='home', is_named_url=True, order=1
        )
        self.about_item = MenuItem.objects.create(
            menu=self.menu, name='About', url='about', is_named_url=True, order=2
        )
        # Non-named URL with a missing reverse name
        self.bad_named = MenuItem.objects.create(
            menu=self.menu, name='Bad', url='no_such', is_named_url=True, order=3
        )
        # Services with child
        self.services_item = MenuItem.objects.create(
            menu=self.menu, name='Services', url='/services/', is_named_url=False, order=4
        )
        self.consulting_item = MenuItem.objects.create(
            menu=self.menu, name='Consulting', url='/services/consulting/', is_named_url=False,
            parent=self.services_item, order=1
        )

    def render_menu(self, path):
        """Helper: render the tag with a fake request path"""
        rf = RequestFactory()
        request = rf.get(path)
        tpl = Template("{% load menu_tags %}{% draw_menu 'main' %}")
        ctx = Context({'request': request})
        return tpl.render(ctx)

    def test_single_db_query(self):
        # Ensure exactly one database query during render
        with self.assertNumQueries(1):
            self.render_menu('/')

    def test_active_named_url(self):
        html = self.render_menu('/')  # home path
        # Home item should be active and open
        self.assertIn('>Home<', html)
        self.assertIn('class="active', html)
        # About should not be active
        self.assertNotIn('>About<', html.replace('>Home<', '>'))

    def test_bad_named_url_fallback(self):
        html = self.render_menu('/')
        # Bad named URL should render with href="#"
        self.assertIn('>Bad<', html)
        self.assertIn('href="#"', html)

    def test_open_ancestors_and_children(self):
        # When viewing '/services/' the Services item is active,
        # its child Consulting should also be open
        html = self.render_menu('/services/')
        # Services should be active and open
        self.assertRegex(html, r'<a href="/services/">Services</a>')
        self.assertIn('class="active open"', html)
        # Consulting (first-level child) should be open
        self.assertRegex(html, r'<li class="open"><a href="/services/consulting/">Consulting</a>')

    def test_named_url_resolution(self):
        # About uses named URL, reverse('about') == '/about/'
        html = self.render_menu('/about/')
        # About link should match reversed URL
        self.assertIn('href="/about/"', html)
        # About item active
        self.assertRegex(html, r'<li class="active open"><a href="/about/">About</a>')

    def test_multiple_menus_independent(self):
        # Create a second menu 'footer' and item
        footer = Menu.objects.create(name='footer')
        footer_item = MenuItem.objects.create(
            menu=footer, name='FooterLink', url='/footer/', is_named_url=False, order=1
        )
        # Render main menu: should not contain FooterLink
        main_html = Template("{% load menu_tags %}{% draw_menu 'main' %}").render(
            Context({'request': RequestFactory().get('/')})
        )
        self.assertNotIn('FooterLink', main_html)
        # Render footer menu: should contain FooterLink
        footer_html = Template("{% load menu_tags %}{% draw_menu 'footer' %}").render(
            Context({'request': RequestFactory().get('/footer/')})
        )
        self.assertIn('FooterLink', footer_html)
        # Only one query per render
        with self.assertNumQueries(1):
            Template("{% load menu_tags %}{% draw_menu 'footer' %}").render(
                Context({'request': RequestFactory().get('/footer/')})
            )
