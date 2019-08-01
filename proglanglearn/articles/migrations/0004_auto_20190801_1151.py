# Generated by Django 2.2.3 on 2019-08-01 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190727_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='auteur'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='contenu'),
        ),
        migrations.AlterField(
            model_name='article',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='article', to='main.Language', verbose_name='langages utilisés'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_modification',
            field=models.DateField(verbose_name='dernière modification'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='article', to='main.Tag', verbose_name='catégories'),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(upload_to='blog_thumbnail/', verbose_name="vignette/vidéo d'article"),
        ),
        migrations.AlterField(
            model_name='article',
            name='timestamp',
            field=models.DateField(verbose_name='date de publication'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=150, verbose_name="titre de l'article"),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='nombre de vues'),
        ),
    ]
