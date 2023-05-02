"""
This file contains the serializers for the core app.
The serializers are used to convert the data from the database to a format that can be easily rendered into JSON or XML format.
"""
from store.models import Customer
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Custom user create serializer.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    """
    Custom user serializer.
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']