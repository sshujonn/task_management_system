# Generated by Django 3.2 on 2021-04-25 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parent_menu', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=50)),
                ('group', models.ManyToManyField(to='auth.Group')),
                ('parent_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parent_menu.parentmenu')),
            ],
        ),
    ]
