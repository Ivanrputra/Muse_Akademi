# Generated by Django 3.1 on 2020-09-03 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20200903_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]