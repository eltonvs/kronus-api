from datetime import time

from clock_in_out.clock.models import ClockEntry
from clock_in_out.users.models import BaseUser


def create_clock_in(*, time: time, user: BaseUser) -> ClockEntry:
    return ClockEntry.objects.create(time=time, user=user, clock_in=None)


def create_clock_out(*, time: time, user: BaseUser, clock_in: int) -> ClockEntry:
    return ClockEntry.objects.create(time=time, user=user, clock_in_id=clock_in)
