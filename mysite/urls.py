from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tsumego/', include('tsumego.urls')),
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
]
