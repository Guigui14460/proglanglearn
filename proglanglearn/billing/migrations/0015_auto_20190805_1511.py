# Generated by Django 2.2.3 on 2019-08-05 13:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_auto_20190804_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='deactivate_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 4, 13, 11, 49, 52319, tzinfo=utc), null=True, verbose_name='date de désactivation du code'),
        ),
    ]