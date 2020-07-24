# Generated by Django 3.0.3 on 2020-07-24 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.IntegerField()),
                ('transaction_url', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('OC', 'Order Created'), ('WP', 'Waiting for Payment'), ('CO', 'Confirmed'), ('CA', 'Canceled'), ('RE', 'Refund'), ('FC', 'Fraud Challenge')], default='OC', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
