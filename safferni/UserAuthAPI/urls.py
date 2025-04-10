from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.api_overview, name='crud_auth_overview'),
    path('get_add_users/', views.UserListCreateAPIView.as_view(), name='get_add_users'),
    path('get_update_delete_user/<int:id>/', views.UserDetailAPIView.as_view(), name='get_update_delete_user_id'),
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),

    # path('logout_instantly/', views.logout, name='logout'),
    # path('auth/', views.LoginRegisterView.as_view(), name='auth'),
    # path('signup/', views.signup, name='signup'),
    # path('signin/', views.login, name='signin'),
    # path('signout/', views.logout, name='signout'),
    # path('test_token/', views.test_token, name='test_token'),
    # path('get_users/', views.get_users, name='get_users'),
    # path('get_users/<str:pk>', views.get_user_detail, name='get_user_id'),
]   