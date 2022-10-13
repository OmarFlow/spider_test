from django.db import models

from .category import Category
from .enterprise import Enterprise, EnterpriseNetwork


class Product(models.Model):
    """Товар."""

    title = models.CharField(verbose_name="Название товара", max_length=100)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE, null=True, related_name="products"
    )
    network = models.ForeignKey(
        EnterpriseNetwork, verbose_name="Сеть", on_delete=models.CASCADE, null=True, related_name="products"
    )
    enterprises = models.ManyToManyField(
        Enterprise, verbose_name="Предприятия")
    last_price = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ProductPrice(models.Model):
    """Цена на товар."""

    price = models.IntegerField(verbose_name="Цена товара")
    enterprise = models.ForeignKey(
        Enterprise, verbose_name="Предприятие", on_delete=models.CASCADE, related_name="prices"
    )
    product = models.ForeignKey(
        Product, verbose_name="Товар", on_delete=models.CASCADE, related_name="prises"
    )

    class Meta:
        verbose_name = "Цена на товар"
        verbose_name_plural = "Цены на товар"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.last_price = self.price
        self.product.save()

    def __str__(self):
        return str(self.price)
