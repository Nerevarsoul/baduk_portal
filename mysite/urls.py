from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tsumego/', include('tsumego.urls')),
    path('tournament/', include('tournament.urls')),
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
]

if True:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
