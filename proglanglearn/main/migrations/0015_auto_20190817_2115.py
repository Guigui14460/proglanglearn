# Generated by Django 2.2.3 on 2019-08-17 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_user_natural_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='natural_language',
            field=models.CharField(max_length=10),
        ),
    ]
