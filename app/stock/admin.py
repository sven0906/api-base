from django.contrib import admin
from stock.models import Stock, StockDetail


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.fields]

@admin.register(StockDetail)
class StockDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StockDetail._meta.fields]
