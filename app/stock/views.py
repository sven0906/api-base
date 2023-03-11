from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from stock.models import Stock
from stock.serializers import StockSerializer
from stock.manager import crawler_dyson_stocks, list_to_html, get_stock_list_for_table, send_mail
from background_task.models import Task
from stock.tasks import add_task_queue


class StockViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
):
    """
    재고관리 뷰
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [
        # IsAuthenticated
    ]

    def list(self, request, *args, **kwargs):
        add_task_queue(repeat=Task.HOURLY * 6)
        # crawler_dyson_stocks(region='ES')
        # items = get_stock_list_for_table()
        # send_mail(items)
        # items = items.order_by("region")
        # send_mail()
        # list_to_html()
        return super().list(request, *args, **kwargs)

