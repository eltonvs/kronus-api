from django.urls import path

from clock_in_out.clock.apis import ClockInApi, ClockLogApi, ClockOutApi

urlpatterns = [
    path('clock-in', ClockInApi.as_view(), name='clock-in'),
    path('clock-out', ClockOutApi.as_view(), name='clock-out'),
    path('log', ClockLogApi.as_view(), name='clock-log'),
]
