from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Enterprise
from ..serializers import EnterpriseDetailSerializer
from spider.services import filter_enterprises


@extend_schema(tags=["Enterprise"])
class EnterpriseViewSet(GenericViewSet):
    queryset = Enterprise.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "organizations":
            return EnterpriseDetailSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer_class()
        return Response(serializer(instance, context={"request": request}).data)

    @action(detail=True, methods=("GET",))
    def organizations(self, request, **kwargs):
        """
        Фильтрация организаций по району и параметру.
        """
        qs = self.queryset.filter(hoods=kwargs["pk"])
        qs_filtered_by_param = filter_enterprises(qs, request.GET)

        serializer = self.get_serializer_class()
        res = serializer(qs_filtered_by_param, many=True).data
        return Response(res)
