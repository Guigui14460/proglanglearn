# Generated by Django 2.2.6 on 2019-12-27 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreport',
            name='type_alert',
            field=models.CharField(choices=[('A', 'Harcèlement'), ('B', 'Discriminations physiques, racistes, sexistes'), ('C', 'Apologie du terrorisme'), ('D', 'Incitations à la violence et à la haine'), ('E', 'Autre (explications demandées)')], max_length=1, verbose_name='type de signalement'),
        ),
    ]
