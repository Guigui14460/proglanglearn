# Generated by Django 2.2.3 on 2019-08-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0024_auto_20190813_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='deactivate_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date de désactivation du code'),
        ),
    ]