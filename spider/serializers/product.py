from rest_framework import serializers

from ..models import Product, ProductPrice, Category, EnterpriseNetwork, Enterprise


class ProductCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    category = serializers.IntegerField()
    network = serializers.IntegerField()
    enterprises = serializers.IntegerField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        title = validated_data.pop('title')
        category = Category.objects.get(id=validated_data.pop('category'))
        network = EnterpriseNetwork.objects.get(
            id=validated_data.pop('network'))
        enterprises = Enterprise.objects.get(
            id=validated_data.pop('enterprises'))
        price = validated_data.pop('price')

        product = Product.objects.create(
            title=title, category=category, network=network)
        product.enterprises.add(enterprises)
        ProductPrice.objects.create(
            product=product, enterprise=enterprises, price=price)
        return product

    class Meta:
        model = Product
        fields = (
            "title",
            "category",
            "network",
            "enterprises",
            "price",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    category = serializers.StringRelatedField()
    network = serializers.StringRelatedField()
    enterprises = serializers.StringRelatedField(many=True)
    price = serializers.IntegerField(source="last_price")

    class Meta:
        model = Product
        fields = (
            "title",
            "category",
            "network",
            "enterprises",
            "price",
        )
