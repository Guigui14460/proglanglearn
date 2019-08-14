# Generated by Django 2.2.3 on 2019-08-11 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190809_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(max_length=50, verbose_name='diplôme obtenu'),
        ),
        migrations.AlterField(
            model_name='education',
            name='entry_date',
            field=models.DateField(verbose_name="date d'entrée dans l'école"),
        ),
        migrations.AlterField(
            model_name='education',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name="date de sortie de l'école"),
        ),
        migrations.AlterField(
            model_name='experience',
            name='entry_date',
            field=models.DateField(verbose_name="date d'arrivée dans l'entreprise"),
        ),
        migrations.AlterField(
            model_name='experience',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name="date de sortie de l'entreprise"),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github_username',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="nom d'utilisateur Github"),
        ),
    ]