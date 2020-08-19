# Generated by Django 3.1 on 2020-08-19 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20200819_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('WP', 'Waiting for Payment'), ('WC', 'Waiting for Confirmation'), ('CO', 'Confirmed'), ('DE', 'Decline')], default='WP', max_length=2),
        ),
    ]
