from rest_framework import serializers

from ..models import Enterprise
from .product import ProductDetailSerializer


class EnterpriseDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    network = serializers.StringRelatedField()
    hoods = serializers.StringRelatedField(many=True)
    product_set = ProductDetailSerializer(many=True)

    class Meta:
        model = Enterprise
        fields = (
            "title",
            "description",
            "network",
            "hoods",
            "product_set",
        )
