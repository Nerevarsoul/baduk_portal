from django.urls import path

from .views import TsumegoResultListView


urlpatterns = [
    path('results/<int:year>/<int:month>', TsumegoResultListView.as_view()),
    path('results/', TsumegoResultListView.as_view()),
]
