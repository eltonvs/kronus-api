from datetime import time
from typing import Optional

from django.db import transaction

from clock_in_out.clock.models import ClockEntry
from clock_in_out.users.models import BaseUser


def create_clock_in(*, time: time, user: BaseUser) -> ClockEntry:
    return ClockEntry.objects.create(time=time, user=user, clock_in=None)


def create_clock_out(*, time: time, user: BaseUser, clock_in: int) -> ClockEntry:
    return ClockEntry.objects.create(time=time, user=user, clock_in_id=clock_in)


@transaction.atomic
def update_clock_entry(
    *, pk: int, time: time, user: BaseUser, out_pk: Optional[int] = None, out_time: Optional[time] = None
):
    # first update clock in and then try to update clock out
    clock_in = ClockEntry.objects.get(pk=pk, user=user)
    clock_in.time = time
    clock_in.save()

    clock_out = None
    if out_pk:
        clock_out = ClockEntry.objects.get(pk=out_pk, user=user)
        clock_out.time = out_time
        clock_out.save()

    return clock_in, clock_out
