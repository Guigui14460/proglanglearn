# Generated by Django 2.2.3 on 2019-07-27 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190715_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name="URL d'accès"),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name="URL d'accès"),
        ),
    ]
