from rest_framework import viewsets

from courses.models import Course, Tutorial
from .serializers import CourseSerializer, TutorialSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class TutorialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Tutorial.objects.get_authorized_tutorials(self.request.user)
    #     return Tutorial.objects.none()
