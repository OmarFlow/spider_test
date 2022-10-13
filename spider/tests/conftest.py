import factory
from pytest_factoryboy import register

from ..models import CityHood, Category, EnterpriseNetwork, Enterprise, Product, ProductPrice


@register
class CityHoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CityHood
    title = factory.Faker("word")


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    title = factory.Faker("word")


@register
class EnterpriseNetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EnterpriseNetwork
    title = factory.Faker("word")


@register
class EnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enterprise
    title = factory.Faker("word")
    description = factory.Faker("words")
    network = factory.SubFactory(EnterpriseNetworkFactory)

    @factory.post_generation
    def hoods(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for hood in extracted:
                self.hoods.add(hood)


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker("word")
    category = factory.SubFactory(CategoryFactory)
    network = factory.SubFactory(EnterpriseNetworkFactory)
    last_price = factory.Faker("pyint")

    @factory.post_generation
    def enterprises(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for enterprise in extracted:
                self.enterprises.add(enterprise)


@register
class ProductPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice
    price = factory.Faker("pyint")
    enterprise = factory.SubFactory(EnterpriseFactory)
    product = factory.SubFactory(ProductFactory)
