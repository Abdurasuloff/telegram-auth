
from django.contrib import admin
from django.urls import path, include
from main.views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),
    path('users/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
