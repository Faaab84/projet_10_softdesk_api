from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthor, IsProjectContributor, IsProjectAuthor

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance)

class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all().order_by('id')
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor | IsProjectContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user).order_by('id')

class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all().order_by('id')
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        return Issue.objects.filter(project__contributors__user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]
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
