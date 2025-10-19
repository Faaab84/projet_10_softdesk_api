from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthor, IsProjectContributor, IsProjectAuthor


class ProjectViewSet(ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les projets.

    Restreint l'accès aux utilisateurs authentifiés qui sont soit l'auteur,
    soit un contributeur du projet.

    Attributes:
        queryset (QuerySet): Projets triés par ID.
        serializer_class (Serializer): Sérialiseur pour les projets.
        permission_classes (list): Permissions (authentification et auteur/contributeur).
    """
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        """
        Filtre les projets pour inclure uniquement ceux où l'utilisateur est contributeur.

        Returns:
            QuerySet: Projets filtrés triés par ID.
        """
        return Project.objects.filter(contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        """
        Crée un projet et ajoute l'utilisateur connecté comme auteur et contributeur.

        Args:
            serializer (Serializer): Sérialiseur contenant les données validées.
        """
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance)


class ContributorViewSet(ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d'un projet.

    Restreint l'accès aux utilisateurs authentifiés qui sont soit l'auteur du projet,
    soit un contributeur.

    Attributes:
        queryset (QuerySet): Contributeurs triés par ID.
        serializer_class (Serializer): Sérialiseur pour les contributeurs.
        permission_classes (list): Permissions (authentification et auteur/contributeur).
    """
    queryset = Contributor.objects.all().order_by('id')
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor | IsProjectContributor]

    def get_queryset(self):
        """
        Filtre les contributeurs pour les projets dont l'utilisateur est l'auteur.

        Returns:
            QuerySet: Contributeurs filtrés triés par ID.
        """
        return Contributor.objects.filter(project__author=self.request.user).order_by('id')


class IssueViewSet(ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les issues.

    Restreint l'accès aux utilisateurs authentifiés qui sont soit l'auteur,
    soit un contributeur du projet associé.

    Attributes:
        queryset (QuerySet): Issues triées par ID.
        serializer_class (Serializer): Sérialiseur pour les issues.
        permission_classes (list): Permissions (authentification et auteur/contributeur).
    """
    queryset = Issue.objects.all().order_by('id')
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        """
        Filtre les issues pour les projets où l'utilisateur est contributeur.

        Returns:
            QuerySet: Issues filtrées triées par ID.
        """
        return Issue.objects.filter(project__contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        """
        Crée une issue avec l'utilisateur connecté comme auteur.

        Args:
            serializer (Serializer): Sérialiseur contenant les données validées.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les commentaires.

    Restreint l'accès aux utilisateurs authentifiés qui sont soit l'auteur,
    soit un contributeur du projet associé à l'issue.

    Attributes:
        queryset (QuerySet): Commentaires triés par ID.
        serializer_class (Serializer): Sérialiseur pour les commentaires.
        permission_classes (list): Permissions (authentification et auteur/contributeur).
        lookup_field (str): Champ utilisé pour identifier les commentaires (UUID).
    """
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        Filtre les commentaires pour les issues des projets où l'utilisateur est contributeur.

        Returns:
            QuerySet: Commentaires filtrés triés par ID.
        """
        return Comment.objects.filter(issue__project__contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        """
        Crée un commentaire avec l'utilisateur connecté comme auteur.

        Args:
            serializer (Serializer): Sérialiseur contenant les données validées.
        """
        serializer.save(author=self.request.user)


class ProjectChoicesView(APIView):
    """
    Vue API pour récupérer les choix de type de projet.

    Renvoie la liste des valeurs possibles pour le champ 'type' du modèle Project.
    """
    def get(self, request):
        """
        Récupère les choix de type de projet.

        Args:
            request (Request): Requête HTTP.

        Returns:
            Response: Liste des valeurs des choix de type.
        """
        return Response({'type': [choice[0] for choice in Project.TYPE_CHOICES]})


class IssueChoicesView(APIView):
    """
    Vue API pour récupérer les choix d'issues.

    Renvoie les valeurs possibles pour les champs 'status', 'priority' et 'tag' du modèle Issue.
    """
    def get(self, request):
        """
        Récupère les choix pour les champs d'issues.

        Args:
            request (Request): Requête HTTP.

        Returns:
            Response: Dictionnaire des valeurs des choix pour status, priority et tag.
        """
        return Response({
            'status': [choice[0] for choice in Issue.STATUS_CHOICES],
            'priority': [choice[0] for choice in Issue.PRIORITY_CHOICES],
            'tag': [choice[0] for choice in Issue.TAG_CHOICES]
        })
