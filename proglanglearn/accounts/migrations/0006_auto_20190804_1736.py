# Generated by Django 2.2.3 on 2019-08-04 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_email_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='education',
            options={'verbose_name': 'éducation', 'verbose_name_plural': 'éducations'},
        ),
        migrations.AlterModelOptions(
            name='experience',
            options={'verbose_name': 'expérience', 'verbose_name_plural': 'expériences'},
        ),
    ]
