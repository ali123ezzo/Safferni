from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('get_add_user', viewset=views.UserView)

urlpatterns = [

    path('', views.api_overview, name='api_over_view'),
    path('signup', views.signup, name='signup'),
    path('signin', views.login, name='signin'),
    path('signout', views.logoutUser, name='signout'),
    path('test_token', views.test_token, name='test_token'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_users/<str:pk>', views.get_user_detail, name='get_users_id'),

    path('', include(router.urls)),
]   