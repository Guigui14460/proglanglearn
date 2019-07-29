# Generated by Django 2.2.3 on 2019-07-29 09:38

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20190728_2202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'coupon promotionnel', 'verbose_name_plural': 'coupons promotionnels'},
        ),
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='123', max_length=20, verbose_name='Code de référence'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coupon',
            name='deactivate_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 28, 9, 37, 30, 541456, tzinfo=utc), null=True, verbose_name='Date de désactivation du code'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='used_by',
            field=models.ManyToManyField(blank=True, related_name='codes', to=settings.AUTH_USER_MODEL, verbose_name='Code utilisé par'),
        ),
    ]
