from django.contrib.auth import get_user_model

from rest_framework import serializers

from main.models import Comment, CommentReport, Language, Tag


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'image', 'content']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'image', 'content']
