from django.urls import path

from .views import TsumegoResultListView


urlpatterns = [
    path('results/', TsumegoResultListView.as_view()),
]
