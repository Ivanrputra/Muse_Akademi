# Generated by Django 3.1 on 2020-09-22 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_auto_20200922_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mitra',
            old_name='name',
            new_name='title',
        ),
    ]
