# Generated by Django 3.1 on 2020-09-01 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.library'),
        ),
    ]
