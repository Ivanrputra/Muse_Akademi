# Generated by Django 3.1 on 2020-08-16 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_auto_20200816_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_type',
        ),
    ]
