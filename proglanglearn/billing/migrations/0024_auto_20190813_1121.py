# Generated by Django 2.2.3 on 2019-08-13 09:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0023_auto_20190813_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='deactivate_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 12, 9, 21, 22, 649051, tzinfo=utc), null=True, verbose_name='date de désactivation du code'),
        ),
    ]