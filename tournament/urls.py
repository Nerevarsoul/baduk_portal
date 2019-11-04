from django.urls import path

from .views import *


urlpatterns = [
    path('tables/<int:id>', SingleTournamentView.as_view()),
]
