"""
Space_Games - URLs principais do projeto
"""
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
    path('api/', include('games.api_urls')),  # URLs para a API REST
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Personalização do Django Admin
admin.site.site_header = '🚀 Space_Games Admin'
admin.site.site_title = 'Space_Games'
admin.site.index_title = 'Painel Administrativo'
