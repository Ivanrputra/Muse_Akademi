# Generated by Django 3.1 on 2020-09-17 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0082_auto_20200917_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='mitra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.mitra'),
        ),
    ]
