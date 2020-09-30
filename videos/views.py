from django.views.generic import ListView

from videos.models import Video


class VideosByTypeListView(ListView):
    template_name = 'videos_list.html'

    def get_queryset(self):
        return Video.objects.filter(kind=self.kwargs.get('kind')).all()
