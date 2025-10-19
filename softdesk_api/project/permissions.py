from rest_framework.permissions import BasePermission
from .models import Project, Contributor, Issue, Comment


class IsAuthor(BasePermission):
    """
    Vérifie si l'utilisateur authentifié est l'auteur de la ressource.
    Appliqué aux modèles Project, Issue, Comment.
    """
    message = "Vous devez être l'auteur pour effectuer cette action."

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est l'auteur de l'objet (Project, Issue, Comment).
        Retourne True si request.user == obj.author, False sinon.
        """
        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """
    Vérifie si l'utilisateur est contributeur du projet associé.
    Appliqué aux modèles Project, Issue, Comment.
    """
    message = "Vous devez être contributeur du projet pour accéder à cette ressource."

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est contributeur du projet lié.
        - Pour Project : vérifie si l'utilisateur est dans les contributeurs.
        - Pour Issue : vérifie si l'utilisateur est contributeur du projet lié.
        - Pour Comment : vérifie si l'utilisateur est contributeur du projet lié à l'issue.
        Retourne True si contributeur, False sinon.
        """
        if not request.user or not request.user.is_authenticated:
            return False

        if isinstance(obj, Project):
            return Contributor.objects.filter(user=request.user, project=obj).exists()
        elif isinstance(obj, Issue):
            return Contributor.objects.filter(user=request.user, project=obj.project).exists()
        elif isinstance(obj, Comment):
            return Contributor.objects.filter(user=request.user, project=obj.issue.project).exists()
        return False


class IsProjectAuthor(BasePermission):
    """
    Vérifie si l'utilisateur est l'auteur du projet.
    Utilisé pour les actions sur les contributeurs (ajout/suppression).
    """
    message = "Vous devez être l'auteur du projet pour gérer les contributeurs."

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est l'auteur du projet lié.
        - Pour Contributor : vérifie si request.user == obj.project.author.
        Retourne True si auteur du projet, False sinon.
        """
        if isinstance(obj, Contributor):
            return obj.project.author == request.user
        return False
