# Generated by Django 2.2.3 on 2019-08-17 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190817_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='natural_language',
            field=models.CharField(max_length=5, verbose_name='langage naturel de cet utilisateur'),
        ),
    ]
