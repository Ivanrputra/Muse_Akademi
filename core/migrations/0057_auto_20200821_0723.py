# Generated by Django 3.1 on 2020-08-21 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20200820_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examproject',
            name='project',
        ),
        migrations.AddField(
            model_name='examproject',
            name='url_project',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
