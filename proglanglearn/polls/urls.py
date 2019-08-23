from django.urls import path

from .views import (
    VoteView,
    PollDetailView,
    PollResultView,
    PollListView,
)


app_name = 'polls'

urlpatterns = [
    path('', PollListView.as_view(), name='poll-list'),
    path('poll/<int:poll_pk>/', PollDetailView.as_view(), name="poll"),
    path('vote/<int:poll_pk>/', VoteView.as_view(), name="poll_ajax_vote"),
    path('result/<int:poll_pk>/', PollResultView.as_view(), name="poll_result"),
]
