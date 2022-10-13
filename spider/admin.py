from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from .models import CityHood, Category, ProductPrice, Product, EnterpriseNetwork, Enterprise


class ProductAdminForm(forms.ModelForm):
    def clean_enterprises(self):
        cleaned_data = super().clean()
        network = cleaned_data.get("network")
        enterprises = cleaned_data.get("enterprises")
        network_enterprises_ids = set(
            network.enterprises.all().values_list("id"))

        if not all(True if (enterprise.id, ) in network_enterprises_ids else False for enterprise in enterprises):
            raise ValidationError("Можно выбрать только предприятия сети")

        return cleaned_data["enterprises"]


class ProductPriceAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data["product"].id:
            raise ValidationError("Сначала создайте товар")
        enterprises = cleaned_data.get("product").enterprises.all()
        enterprise = cleaned_data.get("enterprise")
        enterprises_ids = set(enterprises.values_list("id"))

        if (enterprise.id, ) not in set(enterprises_ids):
            raise ValidationError("Можно выбрать только предприятие товара")

        return cleaned_data


@admin.register(EnterpriseNetwork)
class EnterpriseNetworkAdmin(admin.ModelAdmin):
    ...


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    ...


@admin.register(CityHood)
class CityHoodAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


class ProductPriceAdmin(admin.StackedInline):
    model = ProductPrice
    form = ProductPriceAdminForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['last_price']
    inlines = [ProductPriceAdmin]
    form = ProductAdminForm
