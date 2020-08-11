# Generated by Django 3.1 on 2020-08-10 16:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_examanswer_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examanswer',
            name='report',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
