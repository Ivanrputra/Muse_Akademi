# Generated by Django 3.1 on 2020-08-18 18:02

import core.models_utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20200819_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_pic',
            field=core.models_utils.ContentTypeRestrictedFileFieldProtected(blank=True, null=True, storage=core.models_utils.ProtectedFileSystemStorage(), upload_to=core.models_utils.get_order_attachment_path),
        ),
    ]
