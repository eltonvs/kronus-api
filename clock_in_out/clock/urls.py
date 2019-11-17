from django.urls import path

from clock_in_out.clock.apis import (ChangeClockEntryApi, ClockInApi, ClockLogApi, ClockOutApi)

urlpatterns = [
    path('clock-in', ClockInApi.as_view(), name='clock-in'),
    path('clock-out', ClockOutApi.as_view(), name='clock-out'),
    path('log', ClockLogApi.as_view(), name='clock-log'),
    path('<int:pk>', ChangeClockEntryApi.as_view(), name='change-clock'),
]
