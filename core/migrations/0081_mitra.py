# Generated by Django 3.1 on 2020-09-17 07:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_delete_mitra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mitra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('max_user', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None)),
                ('company_name', models.CharField(max_length=256)),
                ('job_title', models.CharField(max_length=256)),
                ('desc', models.TextField()),
                ('is_valid', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_mitra', to=settings.AUTH_USER_MODEL)),
                ('user', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mitra',
            },
        ),
    ]
