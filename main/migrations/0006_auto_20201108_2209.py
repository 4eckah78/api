# Generated by Django 3.1.2 on 2020-11-08 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201108_1702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worker',
            old_name='avatar_path',
            new_name='avatar',
        ),
    ]