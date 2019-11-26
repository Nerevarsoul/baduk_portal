from django.urls import path

from .views import *


urlpatterns = [
    path('tables/<int:id>', SingleTournamentView.as_view()),
    path('tables/last/<int:title_id>', LastTournamentByTitleView.as_view()),
]
