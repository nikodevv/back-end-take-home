from django.db import models


class Airports(models.Model):
    IATA = models.CharField(
        max_length=3, blank=False, default="000", primary_key=True)


class Routes(models.Model):
    origin = models.ForeignKey(
        Airports,
        on_delete=models.CASCADE,
        related_name='origin')
    destination = models.ForeignKey(
        Airports,
        on_delete=models.CASCADE,
        related_name='destination')