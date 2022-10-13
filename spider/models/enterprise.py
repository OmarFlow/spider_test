from django.db import models

from .hood import CityHood


class EnterpriseNetwork(models.Model):
    """Сеть предприятий."""

    title = models.CharField(verbose_name="Название сети", max_length=100)

    class Meta:
        verbose_name = "Сеть предприятий"
        verbose_name_plural = "Сеть предприятий"

    def __str__(self):
        return self.title


class Enterprise(models.Model):
    """Предприятие."""

    title = models.CharField(
        verbose_name="Название предприятия", max_length=100)
    description = models.TextField(verbose_name="Описание")
    network = models.ForeignKey(
        EnterpriseNetwork, verbose_name="Сеть", on_delete=models.CASCADE, null=True, related_name="enterprises"
    )
    hoods = models.ManyToManyField(CityHood, verbose_name="Районы")

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятии"

    def __str__(self):
        return self.title
