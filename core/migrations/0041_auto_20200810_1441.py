# Generated by Django 3.1 on 2020-08-10 07:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20200810_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None),
        ),
    ]
