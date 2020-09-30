from django.urls import path

from videos.views import VideosByTypeListView


urlpatterns = [
    path('<str:kind>', VideosByTypeListView.as_view(), name='videos'),
]
