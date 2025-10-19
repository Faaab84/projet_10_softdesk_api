from django.db import models
from authentication.models import CustomUser
import uuid


class Project(models.Model):
    """
    Modèle représentant un projet.

    Attributes:
        name (CharField): Nom du projet (max 100 caractères).
        description (TextField): Description facultative du projet.
        type (CharField): Type de projet (choix parmi Back-end, Front-end, iOS, Android).
        author (ForeignKey): Utilisateur ayant créé le projet.
        created_time (DateTimeField): Date et heure de création, automatiquement définies.
    """
    TYPE_CHOICES = (
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Représentation en chaîne du projet.

        Returns:
            str: Nom du projet.
        """
        return self.name


class Contributor(models.Model):
    """
    Modèle représentant un contributeur à un projet.

    Attributes:
        user (ForeignKey): Utilisateur contribuant au projet.
        project (ForeignKey): Projet auquel l'utilisateur contribue.
        created_time (DateTimeField): Date et heure de l'ajout du contributeur.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        """
        Représentation en chaîne du contributeur.

        Returns:
            str: Nom d'utilisateur et nom du projet.
        """
        return f"{self.user.username} on {self.project.name}"


class Issue(models.Model):
    """
    Modèle représentant un problème (issue) dans un projet.

    Attributes:
        title (CharField): Titre du problème (max 100 caractères).
        description (TextField): Description facultative du problème.
        status (CharField): Statut du problème (To Do, In Progress, Finished).
        priority (CharField): Priorité du problème (Low, Medium, High).
        tag (CharField): Type de problème (Bug, Feature, Task).
        project (ForeignKey): Projet associé au problème.
        author (ForeignKey): Utilisateur ayant créé le problème.
        assignee (ForeignKey): Utilisateur assigné au problème, peut être nul.
        created_time (DateTimeField): Date et heure de création.
    """
    STATUS_CHOICES = (
        ('TODO', 'To Do'),
        ('INPROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    TAG_CHOICES = (
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='LOW')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issues')
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Représentation en chaîne du problème.

        Returns:
            str: Titre du problème.
        """
        return self.title


class Comment(models.Model):
    """
    Modèle représentant un commentaire sur un problème.

    Attributes:
        uuid (UUIDField): Identifiant unique du commentaire.
        description (TextField): Contenu du commentaire.
        issue (ForeignKey): Problème associé au commentaire.
        author (ForeignKey): Utilisateur ayant créé le commentaire.
        created_time (DateTimeField): Date et heure de création.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Représentation en chaîne du commentaire.

        Returns:
            str: UUID du commentaire et titre du problème associé.
        """
        return f"Comment {self.uuid} on {self.issue.title}"
