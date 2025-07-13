from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # para django-allauth
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('boards.urls')),  # URL patterns para boards app
    path('', include('tasks.urls', namespace='tasks')),#URL para tareas
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)