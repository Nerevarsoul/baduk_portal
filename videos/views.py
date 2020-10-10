from datetime import datetime

from django.http import Http404
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView

from videos.models import Video


__all__ = ('VideosByTypeListView', 'TsumegoVideosDateList',)


class VideosByTypeListView(ListView):
    template_name = 'videos_list.html'

    def get_queryset(self):
        return Video.objects.filter(kind=self.kwargs.get('kind')).all()


class TsumegoVideosDateList(MonthArchiveView):
    template_name = 'tsumego_videos_date_list.html'
    queryset = Video.objects.filter(kind='tsumego_answer')
    date_field = 'date'
    month_format = '%m'

    def get_month(self):
        try:
            month = super().get_month()
        except Http404:
            month = datetime.now().strftime(self.get_month_format())

        return month

    def get_year(self):
        try:
            year = super().get_year()
        except Http404:
            year = datetime.now().strftime(self.get_year_format())

        return year
