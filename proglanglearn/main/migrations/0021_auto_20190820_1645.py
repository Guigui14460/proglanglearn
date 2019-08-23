# Generated by Django 2.2.3 on 2019-08-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_emailadminnotificationforusers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailadminnotificationforusers',
            options={'ordering': ['-timestamp'], 'verbose_name': "notification par email de l'administration", 'verbose_name_plural': "notifications par email de l'administration"},
        ),
        migrations.AddField(
            model_name='emailadminnotificationforusers',
            name='is_sent',
            field=models.BooleanField(default=False, verbose_name='envoyé'),
        ),
        migrations.AddField(
            model_name='emailadminnotificationforusers',
            name='to_send',
            field=models.BooleanField(default=False, verbose_name='à envoyer'),
        ),
    ]