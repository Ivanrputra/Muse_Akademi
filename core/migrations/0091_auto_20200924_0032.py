# Generated by Django 3.1 on 2020-09-23 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0090_auto_20200923_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mitra',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]