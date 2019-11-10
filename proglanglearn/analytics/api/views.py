from rest_framework import viewsets

from analytics.models import UserExperienceJournal
from .serializers import UserExperienceJournalSerializer


class UserExperienceJournalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserExperienceJournalSerializer
    queryset = UserExperienceJournal.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserExperienceJournal.objects.get_last_journals(self.request.user, 7)
        return UserExperienceJournal.objects.none()
