from rest_framework import serializers

from analytics.models import UserExperienceJournal


class UserExperienceJournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserExperienceJournal
        fields = ['id', 'experience', 'timestamp']
