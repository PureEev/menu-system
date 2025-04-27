from django.db import models
from django.shortcuts import reverse, NoReverseMatch
from django.core.exceptions import ValidationError

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    is_named_url = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=0)
    hierarchy_path = models.CharField(max_length=255, blank=True, editable=False)

    def save(self, *args, **kwargs):
        path = [self.title.replace(' ', '_')]
        current = self.parent
        while current:
            path.append(current.title.replace(' ', '_'))
            current = current.parent
        self.hierarchy_path = '/'.join(reversed(path))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def clean(self):
        if self.url and self.is_named_url:
            raise ValidationError("Нельзя указывать оба URL одновременно")

    def get_url(self):
        if self.is_named_url:
            try:
                return reverse(self.url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

