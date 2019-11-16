from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from clock_in_out.authentication.apis import LoginApi, LogoutApi, UserDetailApi

urlpatterns = [
    path('login', LoginApi.as_view(), name='login'),
    path('me', UserDetailApi.as_view(), name='user-detail'),
    path('logout', LogoutApi.as_view(), name='logout'),
    path('token-refresh', refresh_jwt_token),
]
