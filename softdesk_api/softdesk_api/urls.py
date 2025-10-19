from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
Configuration des URL principales du projet Django.

Ce module définit les routes principales de l'application, incluant l'administration,
les routes de l'API pour l'authentification et les projets, ainsi que les endpoints JWT
pour l'obtention et le rafraîchissement des jetons.

Attributes:
    urlpatterns (list): Liste des chemins d'URL pour le projet.
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('project.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
