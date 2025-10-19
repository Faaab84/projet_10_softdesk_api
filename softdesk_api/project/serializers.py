from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from authentication.models import CustomUser
from authentication.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Project.

    Gère la sérialisation et la désérialisation des projets, incluant l'auteur
    en lecture seule et la création avec l'utilisateur connecté comme auteur.

    Attributes:
        author (UserSerializer): Sérialiseur pour l'auteur, en lecture seule.
        model (Model): Le modèle Project.
        fields (list): Champs inclus dans la sérialisation.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']

    def create(self, validated_data):
        """
        Crée un projet avec l'utilisateur connecté comme auteur.

        Args:
            validated_data (dict): Données validées pour créer le projet.

        Returns:
            Project: Instance du projet créé.
        """
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class ContributorSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Contributor.

    Gère la sérialisation et la désérialisation des contributeurs, avec des clés primaires
    pour l'utilisateur et le projet, et une représentation enrichie pour l'utilisateur.

    Attributes:
        user (PrimaryKeyRelatedField): Clé primaire de l'utilisateur.
        project (PrimaryKeyRelatedField): Clé primaire du projet.
        model (Model): Le modèle Contributor.
        fields (list): Champs inclus dans la sérialisation.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']

    def to_representation(self, instance):
        """
        Personnalise la représentation pour inclure les données de l'utilisateur.

        Args:
            instance (Contributor): Instance du contributeur.

        Returns:
            dict: Représentation sérialisée avec les données de l'utilisateur.
        """
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


class IssueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Issue.

    Gère la sérialisation et la désérialisation des problèmes, incluant l'auteur
    et l'assigné en lecture seule, le projet comme clé primaire, et la création
    avec l'utilisateur connecté comme auteur.

    Attributes:
        author (UserSerializer): Sérialiseur pour l'auteur, en lecture seule.
        assignee (UserSerializer): Sérialiseur pour l'assigné, en lecture seule.
        project (PrimaryKeyRelatedField): Clé primaire du projet.
        model (Model): Le modèle Issue.
        fields (list): Champs inclus dans la sérialisation.
    """
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'tag', 'project', 'author', 'assignee', 'created_time']

    def create(self, validated_data):
        """
        Crée un problème avec l'utilisateur connecté comme auteur.

        Args:
            validated_data (dict): Données validées pour créer le problème.

        Returns:
            Issue: Instance du problème créé.
        """
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Comment.

    Gère la sérialisation et la désérialisation des commentaires, incluant l'auteur
    et l'UUID en lecture seule, le problème comme clé primaire, et la création
    avec l'utilisateur connecté comme auteur.

    Attributes:
        author (UserSerializer): Sérialiseur pour l'auteur, en lecture seule.
        issue (PrimaryKeyRelatedField): Clé primaire du problème.
        uuid (UUIDField): Identifiant unique, en lecture seule.
        model (Model): Le modèle Comment.
        fields (list): Champs inclus dans la sérialisation.
    """
    author = UserSerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'description', 'issue', 'author', 'created_time']

    def create(self, validated_data):
        """
        Crée un commentaire avec l'utilisateur connecté comme auteur.

        Args:
            validated_data (dict): Données validées pour créer le commentaire.

        Returns:
            Comment: Instance du commentaire créé.
        """
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
    