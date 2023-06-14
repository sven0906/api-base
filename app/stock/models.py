from django.db import models


class Stock(models.Model):
    BRAND_CHOICE = (("DY", "Dyson"),)
    REGION_CHOICE = (
        ("UK", "UK"),
        ("FR", "FRANCE"),
        ("IT", "ITALY"),
        ("DE", "Germany"),
        ("US", "USA"),
        ("JP", "JAPAN"),
        ("HK", "HONGKONG"),
        ("KR", "KOREA"),
        ("NL", "NEDERLAND"),
        ("ES", "SPAIN"),
    )
    name = models.CharField("상품명", max_length=200)
    region = models.CharField("지역", max_length=20, choices=REGION_CHOICE, default="uk")
    brand = models.CharField("브랜드", max_length=20, choices=BRAND_CHOICE, default="DY")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def get_stock_checked_time(self):
        return self.stockdetail_set.last().modified_time.strftime("%Y-%m-%d %H:%M:%S")


class StockDetail(models.Model):
    COLOR_CHOICE = (
        (None, None),
        ("Iron", "Iron"),
        ("Copper", "Copper"),
        ("Fuchsia", "Fuchsia"),
        ("Purple", "Purple"),
        ("Red", "Red"),
    )
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    link = models.URLField("링크", null=True)
    color = models.CharField("색깔", max_length=10, choices=COLOR_CHOICE, null=True)
    is_stock = models.BooleanField("재고여부", default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
