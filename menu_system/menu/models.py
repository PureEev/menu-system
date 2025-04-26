# models.py
from django.db import models
from django.utils.text import slugify

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="Будет частью URL")
    url = models.CharField(max_length=200, blank=True,
                           help_text="Если прописан явно, то будет игнорироваться slug")
    is_named_url = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')
    order = models.IntegerField(default=0)

    # Дополнительные поля для контента
    content = models.TextField(blank=True, help_text="HTML или Markdown")
    template_name = models.CharField(
        max_length=200,
        default='menu/home.html',
        help_text="Шаблон для рендеринга контента"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Авто-slug по имени, если не задан
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
