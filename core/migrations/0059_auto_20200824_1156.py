# Generated by Django 3.1 on 2020-08-24 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_course_url_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='url_project',
            new_name='url_meet',
        ),
    ]
