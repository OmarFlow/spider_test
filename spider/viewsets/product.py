from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status

from ..models import Product
from ..serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer

)


@extend_schema(tags=["Products"])
class ProductViewSet(GenericViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()
        return Response(serializer(instance, context={"request": request}).data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
