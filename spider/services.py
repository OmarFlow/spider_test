from typing import Union

from django.http.request import QueryDict
from django.db.models.query import QuerySet
from django.db.models import Min, Max

from spider.models import Enterprise


def filter_enterprises(initial_qs: QuerySet[Enterprise], query_param: QueryDict  # type: ignore
                       ) -> Union['QuerySet[Enterprise]', tuple['QuerySet[Enterprise]']]:
    if query_param.get("category") is not None:
        return initial_qs.filter(product__category=query_param["category"])
    elif query_param.get("min") is not None:
        return (initial_qs.annotate(
            min_price=Min('product__last_price')).order_by('min_price')[0],)
    elif query_param.get("max") is not None:
        return (initial_qs.annotate(
            max_price=Max('product__last_price')).order_by('-max_price')[0],)
    elif query_param.get("product_title") is not None:
        return initial_qs.filter(product__title__search=query_param["product_title"])
