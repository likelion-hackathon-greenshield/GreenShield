from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('green/', include('green.urls')),
    path('', login_view, name='login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)