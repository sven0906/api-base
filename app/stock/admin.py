from django.contrib import admin
from stock.models import Stock, StockDetail


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.fields]

@admin.register(StockDetail)
class StockDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock', 'get_region', 'link', 'color', 'is_stock', 'created_time', 'modified_time']

    @admin.display(description='stock__region')
    def get_region(self, obj):
        return obj.stock.region

