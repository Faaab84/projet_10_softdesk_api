from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser de Django.

    Ce modèle ajoute des champs supplémentaires au modèle utilisateur par défaut pour stocker
    la date de naissance de l'utilisateur et ses préférences concernant les contacts et le partage de données.

    Attributs :
        date_birth (DateField) : La date de naissance de l'utilisateur, facultative.
        can_be_contacted (BooleanField) : Indique si l'utilisateur peut être contacté, par défaut False.
        can_data_be_shared (BooleanField) : Indique si les données de l'utilisateur peuvent être partagées, par défaut
        False.
    """
    date_birth = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
