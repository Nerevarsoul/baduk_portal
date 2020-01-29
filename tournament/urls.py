from django.urls import path

from .views import *


urlpatterns = [
    path('tables/<int:id>', SingleTournamentView.as_view()),
    path('tables/last/<int:title_id>', LastTournamentByTitleView.as_view(), name='last_tournament'),
    path('titles', TournamentTitlesListView.as_view(), name='titles'),
]
