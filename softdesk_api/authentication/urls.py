from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
"""
Configuration des routes pour l'API REST.

Ce module configure les URL pour l'API en utilisant le DefaultRouter de Django REST Framework.
Il enregistre le UserViewSet pour gérer les opérations CRUD sur les utilisateurs.

Attributes:
    router (DefaultRouter): Routeur pour générer les URL de l'API.
    urlpatterns (list): Liste des URL générées par le routeur pour l'API.
"""
