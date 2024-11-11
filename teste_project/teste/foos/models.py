from django.db import models
from django.utils import timezone

from home.models import CustomBaseModel


class Foo(CustomBaseModel):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    is_foo = models.BooleanField(default=False)

