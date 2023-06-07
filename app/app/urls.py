from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from stock.views import TasksCheck

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/stocks/", include("stock.urls")),
    path("tasks/", TasksCheck.as_view()),
    path(
        "robots.txt", lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain")
    ),
]
