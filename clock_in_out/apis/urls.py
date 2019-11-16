from django.urls import include, path

urlpatterns = [path('auth/', include('clock_in_out.authentication.urls'))]
