from django.db import models


class CityHood(models.Model):
    """Район города."""

    title = models.CharField(verbose_name="Название района", max_length=100)

    class Meta:
        verbose_name = "Район города"
        verbose_name_plural = "Районы города"

    def __str__(self):
        return self.title
