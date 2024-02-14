# Project_K/urls.py

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.generic import RedirectView

from Project_K import settings
from clients.views import mark_notification_read

urlpatterns = [
      path('admin/', admin.site.urls),
      re_path(r'^$', RedirectView.as_view(url='/admin/', permanent=False)),  # Redirect root to /admin/
      path('notifications/mark-read/<int:notification_id>/', mark_notification_read,
           name='mark_notification_read'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
