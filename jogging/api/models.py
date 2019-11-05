from django.db import models
from django.utils import timezone

# Create your models here.
class Entry(models.Model):
  distance = models.PositiveIntegerField(default = 0)
  duration = models.PositiveIntegerField(default = 1)
  date = models.DateField(default = timezone.now)