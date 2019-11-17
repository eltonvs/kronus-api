from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from clock_in_out.common.models import UpdatedAtCreatedAtModelMixin
from clock_in_out.users.models import BaseUser


class ClockEntry(UpdatedAtCreatedAtModelMixin):
    user = models.ForeignKey(BaseUser, models.CASCADE)
    time = models.DateTimeField()
    clock_in = models.OneToOneField('self', models.CASCADE, blank=True, null=True, related_name='clock_out')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        clock_type = 'in' if self.clock_in is None else 'out'
        return f'Clock-{clock_type} from {self.user} on {self.time}'

    def clean(self):
        if self.time > timezone.now():
            raise ValidationError("The clock-in/out time can not be in the future")

        is_clock_in = self.clock_in is None
        if is_clock_in:
            # we can only create a new clock-in if there's no "open" clock-in
            open_clock_ins = ClockEntry.objects.filter(user=self.user, clock_in=None, clock_out=None)
            if open_clock_ins.exists():
                raise ValidationError('There is already another clock-in without a clock-out')
            # the clock-in can't overlap with other clock-in/out intervals
            interval_query = ClockEntry.objects.filter(
                user=self.user, clock_in=None, time__lte=self.time, clock_out__time__gte=self.time
            )
            if interval_query.exists():
                raise ValidationError('The clock time is overlapping with another clock-in/out')
        else:
            # the clock-out can't be after the clock-in
            # the clock-out can't be after the clock-in
            if self.time <= self.clock_in.time:
                raise ValidationError('The clock-out time can not be before the clock-in time')
            # the clock-out can't be after the next clock-in
            query = ClockEntry.objects.filter(
                user=self.user, clock_in=None, time__gt=self.clock_in.time, time__lte=self.time
            )
            if query.exists():
                raise ValidationError('The clock-out can not be after the next clock-in')
