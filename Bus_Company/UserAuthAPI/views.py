from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


class UserView(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['GET'])
def get_users(request):
     
	users = User.objects.all().order_by('-id')
	serializer = UserSerializer(users, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def get_user_detail(request, pk):
     
	tasks = User.objects.get(id=pk)
	serializer = UserSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {
        'api url over view' : '/',
		'register a user':'/signup/',
		'sign in':'/signin/',
		'sign out':'/signout/',
		'get all users':'/get_users/',
		'get user by id':'/get_user_detail/',
        'get and add users using a form' : '/get_add_user/'
		}

	return Response(api_urls)

###
@api_view(['POST'])
def signup(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

###
@api_view(['POST'])
def login(request):

    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

###
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    
    return Response("passed!")

###
@api_view(['POST'])
def logoutUser(request):

    logout(request)
    return redirect('login')

