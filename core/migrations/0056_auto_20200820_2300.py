# Generated by Django 3.1 on 2020-08-20 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20200819_2342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['start_at']},
        ),
    ]