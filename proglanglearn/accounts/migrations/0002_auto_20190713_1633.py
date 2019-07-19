# Generated by Django 2.2.3 on 2019-07-13 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorite_articles',
        ),
        migrations.AddField(
            model_name='profile',
            name='favorite_articles',
            field=models.ManyToManyField(blank=True, related_name='article_favorite', to='articles.Article', verbose_name='Articles favoris'),
        ),
    ]