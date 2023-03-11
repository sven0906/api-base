from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from stock.models import Stock
from stock.serializers import StockSerializer
from stock.manager import crawler_dyson_stocks, list_to_html, get_stock_list_for_table, send_mail
from background_task.models import Task
from stock.tasks import task_crawler_dyson, task_send_mail

from stock.tasks import task_crawler_dyson


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
        items = get_stock_list_for_table()
        send_mail(items)
        return Response(status=status.HTTP_200_OK)

