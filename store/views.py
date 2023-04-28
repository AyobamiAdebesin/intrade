from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

# Create your views here.

@api_view(['GET'])
def user_list(request):
    """
    This function handles the request to list all users.
    """
    return Response('Hello, world. You\'re at the users index.')

@api_view()
def user_detail(request, pk):
    """
    This function handles the request to retrieve a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)
    return Response(f'Hello, world. You\'re at the user {user.first_name} detail.')