# Generated by Django 2.2.3 on 2019-08-27 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_education_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='description',
            new_name='description2',
        ),
    ]