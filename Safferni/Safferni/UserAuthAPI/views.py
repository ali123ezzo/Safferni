from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from .models import User
from rest_framework.authtoken.models import Token
from .filters import UserFilter
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import logout, authenticate
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.middleware.csrf import get_token

from django.conf import settings


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {

        'auth_api' : '/',
		'logout' : '/auth/logout/',
		'login' : '/get_users/',
		'register' : '/register/',
        'login or register' : '/auth/',
		'get authenticated user' : '/user/',
        'get and add users only by admins' : '/get_add_user/',
        'get and add users by id only by admins' : '/get_add_user/<str:pk>/',
		}

	return Response(api_urls)


class RegistrationView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            csrf_token = get_token(request)
            
            response_data = {
                'user': {
                    'username': user.username,
                    'email': user.email
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            response = Response(response_data, status=status.HTTP_201_CREATED)
            self._set_secure_cookies(response, refresh, csrf_token)
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _set_secure_cookies(self, response, refresh_token, csrf_token):
        response.set_cookie(
            key='access_token',
            value=str(refresh_token.access_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Strict'
        )
        response.set_cookie(
            key='X-CSRFToken',
            value=csrf_token,
            secure=not settings.DEBUG,
            samesite='Strict'
        )

class LoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            if user:
                refresh = RefreshToken.for_user(user)
                csrf_token = get_token(request)
                
                response_data = {
                    'user': {
                        'username': user.username,
                        'email': user.email
                    },
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                
                response = Response(response_data, status=status.HTTP_200_OK)
                self._set_secure_cookies(response, refresh, csrf_token)
                return response
            
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _set_secure_cookies(self, response, refresh_token, csrf_token):
        response.set_cookie(
            key='access_token',
            value=str(refresh_token.access_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Strict'
        )
        response.set_cookie(
            key='X-CSRFToken',
            value=csrf_token,
            secure=not settings.DEBUG,
            samesite='Strict'
        )
  

class LogoutView(APIView):
    """
    Handles user logout by:
    1. Blacklisting refresh token
    2. Clearing authentication cookies
    3. Providing CSRF protection
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get refresh token from request data
            refresh_token = request.data.get('refresh')
            
            # If we have a refresh token, blacklist it
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Prepare response
            response = Response(
                {'detail': 'Successfully logged out'},
                status=status.HTTP_205_RESET_CONTENT
            )
            
            # Clear the access token cookie
            self._clear_cookies(response)
            
            return response
        
        except TokenError as e:
            return Response(
                {'error': 'Invalid token', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Logout failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _clear_cookies(self, response):
        """Helper method to clear authentication cookies"""
        cookie_names = [
            settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'),
            'X-CSRFToken',
        ]
        
        for cookie_name in cookie_names:
            response.delete_cookie(
                cookie_name,
                path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
                domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN')
            )


@api_view(['POST'])
def logout(request):

    logout(request)
    return redirect('login')



class UserListCreateAPIView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    filterset_class = UserFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST' or self.request.method == 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    lookup_field = 'id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE', 'GET']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()    
  

class UserDetailView(APIView):
    """
    Get user details
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserRegistrationSerializer(request.user)
        return Response(serializer.data)
  
# class LoginRegisterView(APIView):
#     """
#     Handles both registration and login
#     """
#     permission_classes = [AllowAny]
    
#     def post(self, request, *args, **kwargs):
#         action = request.data.get('action')
        
#         if action == 'register':
#             return self._handle_registration(request)
#         elif action == 'login':
#             return self._handle_login(request)
#         else:
#             return Response(
#                 {'error': 'Action not recognized'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
    
#     def _handle_registration(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             if user:
#                 # Generate tokens
#                 refresh = RefreshToken.for_user(user)
#                 csrf_token = get_token(request)
                
#                 response_data = {
#                     'user': UserSerializer(user).data,
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
                
#                 response = Response(response_data, status=status.HTTP_201_CREATED)
                
#                 # Set secure cookies if in production
#                 if not settings.DEBUG:
#                     self._set_secure_cookies(response, refresh, csrf_token)
                
#                 return response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def _handle_login(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         user = authenticate(username=username, password=password)
        
#         if user:
#             refresh = RefreshToken.for_user(user)
#             csrf_token = get_token(request)
            
#             response_data = {
#                 'user': UserSerializer(user).data,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
            
#             response = Response(response_data, status=status.HTTP_200_OK)
            
#             # Set secure cookies if in production
#             if not settings.DEBUG:
#                 self._set_secure_cookies(response, refresh, csrf_token)
            
#             return response
        
#         return Response(
#             {'error': 'Invalid credentials'}, 
#             status=status.HTTP_401_UNAUTHORIZED
#         )
    
#     def _set_secure_cookies(self, response, refresh_token, csrf_token):
#         response.set_cookie(
#             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#             value=str(refresh_token.access_token),
#             expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#             secure=True,
#             httponly=True,
#             samesite='Strict',
#             path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
#         )
#         response.set_cookie(
#             key='X-CSRFToken',
#             value=csrf_token,
#             secure=True,
#             httponly=False,  # JavaScript needs to read this
#             samesite='Strict'
#         )


# @api_view(['POST'])
# def signup(request):

#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_200_OK)


# # normal user login
# @api_view(['POST'])
# def login(request):

#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response("missing user", status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(user)
#     return Response({'token': token.key, 'user': serializer.data})



