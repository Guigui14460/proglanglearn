from django.contrib.auth import get_user_model

from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from articles.api.views import ArticleViewSet


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('articles', ArticleViewSet)
