# Generated by Django 2.2.3 on 2019-08-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190819_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAdminNotificationForUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='sujet')),
                ('subject_fr', models.CharField(max_length=100, null=True, verbose_name='sujet')),
                ('subject_en', models.CharField(max_length=100, null=True, verbose_name='sujet')),
                ('body', models.TextField(verbose_name='corps')),
                ('body_fr', models.TextField(null=True, verbose_name='corps')),
                ('body_en', models.TextField(null=True, verbose_name='corps')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name="date d'envoi")),
            ],
        ),
    ]
