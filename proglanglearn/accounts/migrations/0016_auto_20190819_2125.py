# Generated by Django 2.2.3 on 2019-08-19 19:25

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20190819_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='description',
            field=tinymce.models.HTMLField(default='default', verbose_name="description de l'emploi"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experience',
            name='employment',
            field=models.CharField(max_length=100, verbose_name="type de l'emploi"),
        ),
    ]
