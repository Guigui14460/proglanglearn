# Generated by Django 2.2.6 on 2019-11-02 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='auteur'),
        ),
        migrations.AddField(
            model_name='course',
            name='languages',
            field=models.ManyToManyField(to='main.Language', verbose_name='langages utilisés'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='étudiants enrollés'),
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(blank=True, to='main.Tag', verbose_name='catégories'),
        ),
    ]
