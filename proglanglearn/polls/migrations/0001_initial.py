# Generated by Django 2.2.6 on 2019-11-02 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, verbose_name='valeur')),
                ('value_fr', models.CharField(max_length=200, null=True, verbose_name='valeur')),
                ('value_en', models.CharField(max_length=200, null=True, verbose_name='valeur')),
                ('position', models.SmallIntegerField(default=0, verbose_name='position')),
                ('votes', models.PositiveIntegerField(default=0, verbose_name='nombre de votes')),
            ],
            options={
                'verbose_name': 'réponse de sondage',
                'verbose_name_plural': 'réponses de sondage',
                'ordering': ['poll', 'position'],
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='question')),
                ('title_fr', models.CharField(max_length=250, null=True, verbose_name='question')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='question')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='date de fin')),
                ('is_published', models.BooleanField(blank=True, default=True, verbose_name='est publié')),
                ('votes', models.PositiveIntegerField(default=0, verbose_name='nombre de votes')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'sondage',
                'verbose_name_plural': 'sondages',
                'ordering': ['-date', '-end_date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name="adresse IP de l'utilisateur")),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Item', verbose_name='valeur votée')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to='polls.Poll', verbose_name='sondage associé')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='utilisateur associé')),
            ],
            options={
                'verbose_name': 'vote de sondage',
                'verbose_name_plural': 'votes de sondage',
                'ordering': ['poll', '-datetime'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='polls.Poll', verbose_name='sondage asscoié'),
        ),
    ]
