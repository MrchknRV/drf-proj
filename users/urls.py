from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("profile/", views.UserDetailAPIView.as_view(), name="user-profile"),
    path("profile/update/", views.UserUpdateAPIView.as_view(), name="user-update"),
    path("profile/delete/", views.UserDeleteAPIView.as_view(), name="user-delete"),
]
