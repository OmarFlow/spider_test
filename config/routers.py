from rest_framework.routers import DefaultRouter

from spider.viewsets import ProductViewSet, EnterpriseViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"enterprises", EnterpriseViewSet, basename="enterprises")
