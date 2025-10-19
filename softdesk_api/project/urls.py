from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'projects/(?P<project_id>\d+)/contributors', ContributorViewSet, basename='contributor')
router.register(r'projects/(?P<project_id>\d+)/issues', IssueViewSet, basename='issue')
router.register(r'projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
