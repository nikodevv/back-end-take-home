from django.db import models


class Routes(models.Model):
    origin = models.CharField(max_length=3, blank=False, default="000")
    destination = models.CharField(
        max_length=3, blank=False, default="000")
