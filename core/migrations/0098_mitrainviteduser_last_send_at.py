# Generated by Django 3.1 on 2020-10-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_auto_20200929_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitrainviteduser',
            name='last_send_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]