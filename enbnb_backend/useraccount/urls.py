from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view #get refresh token
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView
from . import api

urlpatterns = [
  path('register/', RegisterView.as_view(), name='user_register'),
  path('login/', LoginView.as_view(), name='user_login'),
  path('logout/', LogoutView.as_view(), name='user_logout'),
  path('<uuid:pk>/', api.get_host_details, name='get_host_details'),
  path('user/favorite/<uuid:pk>/', api.toggle_favorite, name='toggle_favorite'),
]