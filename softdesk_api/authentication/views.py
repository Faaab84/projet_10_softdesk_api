from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle CustomUser.

    Ce ViewSet fournit des endpoints pour créer, lire, mettre à jour et supprimer des utilisateurs.
    Les permissions sont configurées pour exiger une authentification, sauf pour les actions
    'create' (inscription) et 'list' (liste des utilisateurs).

    Attributes:
        queryset (QuerySet): Ensemble des objets CustomUser.
        serializer_class (Serializer): Sérialiseur utilisé pour les données utilisateur.
        permission_classes (list): Permissions par défaut (authentification requise).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action.

        Permet un accès non authentifié pour les actions 'create' et 'list',
        sinon applique les permissions par défaut.

        Returns:
            list: Liste des permissions appliquées pour l'action courante.
        """
        if self.action in ['create', 'list']:
            return []
        return super().get_permissions()
