# Generated by Django 2.2.3 on 2019-08-13 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20190808_2303'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='languages',
            field=models.ManyToManyField(related_name='subject', to='main.Language', verbose_name='langages utilisés'),
        ),
        migrations.AddField(
            model_name='subject',
            name='tags',
            field=models.ManyToManyField(related_name='subject', to='main.Tag', verbose_name='catégories du sujet'),
        ),
    ]
