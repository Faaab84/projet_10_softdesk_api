from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet, ProjectChoicesView, IssueChoicesView

"""
Configuration des routes pour l'API SoftDesk.

Ce module utilise DefaultRouter pour enregistrer les ViewSets des modèles
Project, Contributor, Issue et Comment, et définit des chemins supplémentaires
pour les vues de choix de projets et d'issues.

Attributes:
    router (DefaultRouter): Routeur pour générer les URL des ViewSets.
    urlpatterns (list): Liste des URL combinant les routes du routeur et les chemins personnalisés.
"""
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'projects/(?P<project_id>\d+)/contributors', ContributorViewSet, basename='contributor')
router.register(r'projects/(?P<project_id>\d+)/issues', IssueViewSet, basename='issue')
router.register(r'projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = router.urls + [
    path('choices/projects/', ProjectChoicesView.as_view(), name='project-choices'),
    path('choices/issues/', IssueChoicesView.as_view(), name='issue-choices'),
]
