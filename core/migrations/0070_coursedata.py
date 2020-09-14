# Generated by Django 3.1 on 2020-09-11 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_library_is_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('course_type', models.CharField(choices=[('AU', 'Semua User'), ('MO', 'Hanya untuk user mitra yang terdaftar')], default='AU', max_length=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_data',
            },
        ),
    ]