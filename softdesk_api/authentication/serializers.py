from rest_framework import serializers
from .models import CustomUser
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle CustomUser.
    Ce sérialiseur gère la sérialisation et la désérialisation des données utilisateur,
    incluant la création d'utilisateurs et la validation de la date de naissance.
    Les mots de passe sont marqués comme write-only pour des raisons de sécurité.
    Attributes:
        model (Model): Le modèle associé, CustomUser.
        fields (list): Les champs à inclure dans la sérialisation.
        extra_kwargs (dict): Configuration supplémentaire pour les champs, comme write_only pour le mot de passe.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'date_birth', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.
        Args:
            validated_data (dict): Données validées pour créer l'utilisateur.
        Returns:
            CustomUser: Instance de l'utilisateur créé.
        """
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate_date_birth(self, value):
        """
        Valide la date de naissance pour s'assurer que l'utilisateur a au moins 15 ans.
        Args:
            value (date): La date de naissance à valider.
        Returns:
            date: La date de naissance validée.
        Raises:
            serializers.ValidationError: Si l'utilisateur a moins de 15 ans.
        """
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value
