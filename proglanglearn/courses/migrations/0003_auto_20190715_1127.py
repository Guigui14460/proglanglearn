# Generated by Django 2.2.3 on 2019-07-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20190713_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-published_date', 'title'], 'verbose_name': 'cours', 'verbose_name_plural': 'cours'},
        ),
        migrations.AlterModelOptions(
            name='tutorial',
            options={'ordering': ['-views', 'title', 'experience'], 'verbose_name': 'tutoriel'},
        ),
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.URLField(blank=True, null=True, verbose_name="URL d'accès"),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='slug',
            field=models.URLField(blank=True, null=True, verbose_name="URL d'accès"),
        ),
    ]
