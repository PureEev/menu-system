# Generated by Django 5.2 on 2025-04-26 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_rename_name_menuitem_title_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='slug',
        ),
    ]
