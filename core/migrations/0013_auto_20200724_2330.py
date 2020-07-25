# Generated by Django 3.0.3 on 2020-07-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ManyToManyField(to='core.Category'),
        ),
    ]
