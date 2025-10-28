from rest_framework.permissions import BasePermission
from .models import Project, Contributor, Issue, Comment


def check_contributor(user, project):
    """Vérifie si l'utilisateur est contributeur du projet."""
    if not project or not user:
        return False
    return Contributor.objects.filter(project=project, user=user).exists()


class IsAuthor(BasePermission):
    """Vérifie si l'utilisateur est l'auteur de l'objet (Issue, Comment, etc.)."""
    message = "Vous devez être l'auteur pour effectuer cette action."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """Vérifie si l'utilisateur est contributeur du projet associé."""
    message = "Vous devez être contributeur du projet pour accéder à cette ressource."

    def has_permission(self, request, view):
        """Pour les actions sans objet (list, create)"""
        if not request.user or not request.user.is_authenticated:
            return False

        project_id = None
        if 'project_id' in view.kwargs:
            project_id = view.kwargs['project_id']
        elif 'projects_pk' in view.kwargs:
            project_id = view.kwargs['projects_pk']

        if view.action == 'create':
            if not project_id:
                if request.data.get('project'):
                    project_id = request.data.get('project')
                elif request.data.get('issue'):
                    issue_id = request.data.get('issue')
                    issue = Issue.objects.filter(id=issue_id).first()
                    if issue:
                        project_id = issue.project.id
            if not project_id:
                return True  # Pour la création de projet
        elif view.action == 'list':
            if not project_id:
                return True  # Pour la liste globale, filtrée par queryset

        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        return check_contributor(request.user, project)

    def has_object_permission(self, request, view, obj):
        """Pour les actions avec objet (retrieve, update, destroy)"""
        if not request.user or not request.user.is_authenticated:
            return False

        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author == request.user

        if isinstance(obj, Project):
            project = obj
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Comment):
            project = obj.issue.project
        else:
            return False

        return check_contributor(request.user, project)


class IsProjectAuthor(BasePermission):
    """Vérifie si l'utilisateur est l'auteur du projet (pour gérer les contributeurs)."""
    message = "Vous devez être l'auteur du projet pour gérer les contributeurs."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        project_id = None
        if 'project_id' in view.kwargs:
            project_id = view.kwargs['project_id']
        elif 'projects_pk' in view.kwargs:
            project_id = view.kwargs['projects_pk']

        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        return request.user == project.author

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.author == request.user
        if isinstance(obj, Contributor):
            return obj.project.author == request.user
        return False
