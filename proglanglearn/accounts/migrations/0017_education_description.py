# Generated by Django 2.2.3 on 2019-08-27 10:31

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20190819_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='description',
            field=tinymce.models.HTMLField(default='', verbose_name='description'),
            preserve_default=False,
        ),
    ]
