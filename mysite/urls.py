from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path('', TemplateView.as_view(template_name="homepage.html"), name='homepage'),
    path('news/', TemplateView.as_view(template_name="in_progress.html"), name='news'),
    path('lessons/', TemplateView.as_view(template_name="in_progress.html"), name='lessons'),
    path('contacts/', TemplateView.as_view(template_name="in_progress.html"), name='contacts'),
    path('videos/', include('videos.urls')),
    path('admin/', admin.site.urls),
    path('tsumego/', include('tsumego.urls')),
    path('tournament/', include('tournament.urls')),
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
]

if True:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
