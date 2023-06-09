from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from stock.models import Stock
from stock.serializers import StockSerializer
from stock.manager import crawler_dyson_stocks, list_to_html, get_stock_list_for_table, send_mail

from stock.tasks import task_send_mail, task_crawler_dyson
from background_task.models import Task


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
        region = request.GET.get("region")
        if region:
            crawler_dyson_stocks(region)
        else:
            items = get_stock_list_for_table()
            send_mail(items)
        return Response(status=status.HTTP_200_OK)


class TasksCheck(APIView):
    def get(self, request):
        task_send_mail(repeat=Task.DAILY)
        task_crawler_dyson(repeat=Task.HOURLY)

        return Response(status=status.HTTP_302_FOUND)
