from django.urls import include, path

urlpatterns = [
    path('auth/', include('clock_in_out.authentication.urls')),
    path('users/', include('clock_in_out.users.urls')),
    path('clock/', include('clock_in_out.clock.urls')),
]
