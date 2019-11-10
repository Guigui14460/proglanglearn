from rest_framework import serializers

from courses.models import Course, Tutorial


class TutorialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tutorial
        fields = ['id', 'course', 'title',
                  'content', 'resources',
                  'experience', 'views',
                  'published_date']


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    all_experience = serializers.IntegerField(source='get_all_experience')
    downloadable_ressources = serializers.IntegerField(
        source='get_all_downloadable_resources')
    percentage_discount = serializers.IntegerField(
        source='get_percentage_discount')

    class Meta:
        model = Course
        fields = ['id', 'author', 'title',
                  'thumbnail', 'languages', 'tags',
                  'difficulty', 'content_introduction',
                  'pdf', 'published_date', 'old_price',
                  'new_price', 'all_experience', 'downloadable_ressources',
                  'percentage_discount', 'tutorial', 'students']
