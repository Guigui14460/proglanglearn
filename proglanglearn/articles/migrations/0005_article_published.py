# Generated by Django 2.2.3 on 2019-08-17 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20190801_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False, verbose_name='article publié'),
        ),
    ]