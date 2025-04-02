from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.login, name='signin'),
    path('signout', views.logoutUser, name='signout'),
    path('test_token', views.test_token, name='test_token'),
]   