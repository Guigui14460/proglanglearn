from django.urls import path

from .session_views import SessionDeleteOtherView, SessionDeleteView, SessionListView


urlpatterns = [
    path('', SessionListView.as_view(), name='session_list'),
    path('other/delete/', SessionDeleteOtherView.as_view(),
         name='session_delete_other'),
    path('<str:pk>/delete/', SessionDeleteView.as_view(), name='session_delete'),
]
