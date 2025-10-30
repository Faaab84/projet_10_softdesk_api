from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsProjectContributor, IsProjectAuthor


class ProjectViewSet(ModelViewSet):

    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectContributor]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance)


class ContributorViewSet(ModelViewSet):
    """ViewSet pour gérer les contributeurs d'un projet."""
    queryset = Contributor.objects.all().order_by('id')
    serializer_class = ContributorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = [IsProjectContributor]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project_id=project_id).order_by('id')


class IssueViewSet(ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les issues."""
    queryset = Issue.objects.all().order_by('id')
    serializer_class = IssueSerializer
    permission_classes = [IsProjectContributor]

    def get_queryset(self):
        return Issue.objects.filter(project__contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les commentaires."""
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsProjectContributor]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectChoicesView(APIView):
    def get(self, request):
        return Response({'type': [choice[0] for choice in Project.TYPE_CHOICES]})


class IssueChoicesView(APIView):


    def get(self, request):
        return Response({
            'status': [choice[0] for choice in Issue.STATUS_CHOICES],
            'priority': [choice[0] for choice in Issue.PRIORITY_CHOICES],
            'tag': [choice[0] for choice in Issue.TAG_CHOICES]
        })


class IssueDetailView(APIView):
    """Gère GET, PUT, PATCH, DELETE pour une issue spécifique."""
    permission_classes = [IsProjectContributor]


    def _get_project_and_issue(self, project_id, issue_id):
        project = get_object_or_404(Project, pk=project_id)
        issue = get_object_or_404(Issue, pk=issue_id, project=project)
        return project, issue

    def get(self, request, project_id, issue_id):
        try:
            project, issue = self._get_project_and_issue(project_id, issue_id)
        except Http404:
            return Response({"detail": "Issue non trouvée."}, status=404)
        # Vérifie la permission → 403 si non contributeur
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=200)

    def put(self, request, project_id, issue_id):
        try:
            project, issue = self._get_project_and_issue(project_id, issue_id)
        except Http404:
            return Response({"detail": "Issue non trouvée."}, status=404)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, project_id, issue_id):
        try:
            project, issue = self._get_project_and_issue(project_id, issue_id)
        except Http404:
            return Response({"detail": "Issue non trouvée."}, status=404)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, issue_id):
        try:
            project, issue = self._get_project_and_issue(project_id, issue_id)
        except Http404:
            return Response({"detail": "Issue non trouvée."}, status=404)
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response(status=204)
