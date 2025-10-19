from rest_framework import serializers
from .models import CustomUser
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'date_birth', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


    def validate_date_birth(self, value):
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value
