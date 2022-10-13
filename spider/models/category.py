from django.db import models


class Category(models.Model):
    """Категория."""

    title = models.CharField(verbose_name="Название категории", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title
