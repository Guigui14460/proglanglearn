from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'title',
                  'thumbnail', 'languages',
                  'tags', 'content', 'views',
                  'timestamp', 'last_modification']
