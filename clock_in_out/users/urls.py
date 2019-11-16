from django.urls import path

from clock_in_out.users.apis import SignupApi

urlpatterns = [
    path('', SignupApi.as_view(), name='signup'),
]
