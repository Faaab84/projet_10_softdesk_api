from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser
from project.models import Project, Contributor, Issue, Comment
from datetime import date
import uuid

# Create your tests here.


class SoftDeskAPITestCase(APITestCase):
    def setUp(self):
        # Créer des utilisateurs de test
        self.admin = CustomUser.objects.create_superuser(
            username='admin_test',
            password='adminpass123',
            email='admin@test.com',
            date_birth=date(1990, 1, 1),
            can_be_contacted=True,
            can_data_be_shared=True
        )
        self.user1 = CustomUser.objects.create_user(
            username='alice',
            password='userpass789',
            email='alice@test.com',
            date_birth=date(1995, 1, 1),
            can_be_contacted=True,
            can_data_be_shared=True
        )
        self.user2 = CustomUser.objects.create_user(
            username='bob',
            password='userpass789',
            email='bob@test.com',
            date_birth=date(1998, 1, 1),
            can_be_contacted=True,
            can_data_be_shared=True
        )
        # Créer un projet avec user1 comme auteur
        self.project = Project.objects.create(
            name='Test Project',
            description='Un projet de test',
            type='BACKEND',
            author=self.user1
        )
        # Ajouter user1 comme contributeur
        Contributor.objects.create(user=self.user1, project=self.project)
        # Créer une issue
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='Une issue de test',
            status='TODO',
            priority='HIGH',
            tag='BUG',
            project=self.project,
            author=self.user1,
            assignee=self.user1
        )
        # Créer un commentaire
        self.comment = Comment.objects.create(
            description='Test Comment',
            issue=self.issue,
            author=self.user1
        )

    def get_token(self, username, password):
        """Obtenir un access_token pour un utilisateur."""
        response = self.client.post(
            '/api/token/',
            {'username': username, 'password': password},
            format='json'
        )
        return response.data['access']

    def test_project_crud_author(self):
        """Test CRUD pour Project par l'auteur."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Créer
        response = self.client.post(
            '/api/projects/',
            {'name': 'Nouveau Projet', 'description': 'Test', 'type': 'FRONTEND'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Lister (pagination)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)  # PAGE_SIZE

        # Mettre à jour
        project_id = response.data['results'][0]['id']
        response = self.client.put(
            f'/api/projects/{project_id}/',
            {'name': 'Projet Modifié', 'description': 'Modifié', 'type': 'BACKEND'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Supprimer
        response = self.client.delete(f'/api/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_access_non_contributor(self):
        """Test accès à Project par un non-contributeur."""
        token = self.get_token('bob', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # Liste vide

    def test_project_access_unauthenticated(self):
        """Test accès à Project sans authentification."""
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contributor_crud_author(self):
        """Test CRUD pour Contributor par l'auteur du projet."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Ajouter un contributeur
        response = self.client.post(
            f'/api/projects/{self.project.id}/contributors/',
            {'user': self.user2.id, 'project': self.project.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Lister
        response = self.client.get(f'/api/projects/{self.project.id}/contributors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

        # Supprimer
        contributor_id = Contributor.objects.filter(user=self.user2, project=self.project).first().id
        response = self.client.delete(f'/api/projects/{self.project.id}/contributors/{contributor_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_issue_crud_author(self):
        """Test CRUD pour Issue par l'auteur."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Créer
        response = self.client.post(
            f'/api/projects/{self.project.id}/issues/',
            {
                'title': 'Nouvelle Issue',
                'description': 'Test',
                'status': 'TODO',
                'priority': 'LOW',
                'tag': 'FEATURE',
                'project': self.project.id,
                'assignee': self.user1.id
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Lister (pagination)
        response = self.client.get(f'/api/projects/{self.project.id}/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)

        # Mettre à jour
        issue_id = response.data['results'][0]['id']
        response = self.client.put(
            f'/api/projects/{self.project.id}/issues/{issue_id}/',
            {
                'title': 'Issue Modifiée',
                'description': 'Modifié',
                'status': 'INPROGRESS',
                'priority': 'MEDIUM',
                'tag': 'TASK',
                'project': self.project.id,
                'assignee': self.user1.id
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Supprimer
        response = self.client.delete(f'/api/projects/{self.project.id}/issues/{issue_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_crud_author(self):
        """Test CRUD pour Comment par l'auteur."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Créer
        response = self.client.post(
            f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
            {'description': 'Nouveau Commentaire', 'issue': self.issue.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Lister (pagination)
        response = self.client.get(f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)

        # Mettre à jour
        comment_uuid = response.data['results'][0]['uuid']
        response = self.client.put(
            f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment_uuid}/',
            {'description': 'Commentaire Modifié', 'issue': self.issue.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Supprimer
        response = self.client.delete(f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_choices_read_only(self):
        """Test endpoints read-only pour les choix."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # GET choices pour Project
        response = self.client.get('/api/choices/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('type', response.data)

        # POST interdit
        response = self.client.post('/api/choices/projects/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # GET choices pour Issue
        response = self.client.get('/api/choices/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('priority', response.data)
        self.assertIn('tag', response.data)

    def test_pagination(self):
        """Test pagination pour les listes."""
        token = self.get_token('alice', 'userpass789')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Créer plusieurs projets
        for i in range(15):
            self.client.post(
                '/api/projects/',
                {'name': f'Projet {i}', 'description': 'Test', 'type': 'BACKEND'},
                format='json'
            )

        # Tester pagination
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # PAGE_SIZE
        self.assertIsNotNone(response.data['next'])

        # Accéder à la page 2
        response = self.client.get('/api/projects/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['previous'])
