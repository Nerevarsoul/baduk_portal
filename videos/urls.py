from django.urls import path

from videos.views import *


urlpatterns = [
    path(
        'tsumego_videos_date_list',
         TsumegoVideosDateList.as_view(),
        name='current_tsumego_videos_date_list'
    ),
    path(
        'tsumego_videos_date_list/<int:year>/<int:month>/',
        TsumegoVideosDateList.as_view(),
        name='tsumego_videos_date_list'
    ),
    path('<str:kind>', VideosByTypeListView.as_view(), name='videos')
]
