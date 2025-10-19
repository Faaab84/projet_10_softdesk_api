from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthor, IsProjectContributor, IsProjectAuthor


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=serializer.instance)


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor | IsProjectContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        return Issue.objects.filter(project__contributors__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsProjectContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue__project__contributors__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
