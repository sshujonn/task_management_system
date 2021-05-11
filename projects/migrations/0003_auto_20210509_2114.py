# Generated by Django 3.1.7 on 2021-05-09 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_auto_20210509_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='last_updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
