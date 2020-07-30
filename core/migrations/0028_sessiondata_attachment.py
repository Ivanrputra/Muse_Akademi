# Generated by Django 3.0.3 on 2020-07-30 17:51

import core.models_utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200731_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiondata',
            name='attachment',
            field=core.models_utils.ContentTypeRestrictedFileFieldProtected(default='', storage=core.models_utils.ProtectedFileSystemStorage(), upload_to=core.models_utils.get_session_attachment_path),
            preserve_default=False,
        ),
    ]
