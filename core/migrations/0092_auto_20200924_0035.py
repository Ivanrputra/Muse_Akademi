# Generated by Django 3.1 on 2020-09-23 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0091_auto_20200924_0032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mitra',
            old_name='admin',
            new_name='user_admin',
        ),
    ]
