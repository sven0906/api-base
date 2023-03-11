from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "stock"

router = routers.DefaultRouter()
router.register(r"", views.StockViewSet, basename="stocks")


urlpatterns = [
    path("", include(router.urls)),
]
