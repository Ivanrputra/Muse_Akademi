# Generated by Django 3.0.3 on 2020-07-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_sessiondata_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='examproject',
            name='title',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
