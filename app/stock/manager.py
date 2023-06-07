import logging
import time
import requests
from django.core.mail import EmailMessage
from stock.models import Stock, StockDetail

logger = logging.getLogger(__name__)

DYSON_NAME = {
    "New Coanda smoothing dryer(Nickel / Iron)": "coanda-smoothing-dryer-iron-nickel",
    "New Coanda smoothing dryer(Nickel / Copper)": "coanda-smoothing-dryer-iron-copper",
    "New Coanda smoothing dryer(Nickel / Fuchsia)": "coanda-smoothing-dryer-iron-fuchsia",
    "New 40mm Airwrap™ long barrel(Nickel / Iron)": "40mm-airwrap-long-barrel-iron-nickel",
    "New 40mm Airwrap™ long barrel(Nickel / Copper)": "40mm-airwrap-long-barrel-iron-copper",
    "New 40mm Airwrap™ long barrel(Nickel / Fuchsia)": "40mm-airwrap-long-barrel-iron-fuchsia",
    "New 30mm Airwrap™ long barrel(Nickel / Iron)": "30mm-airwrap-long-barrel-iron-nickel",
    "New 30mm Airwrap™ long barrel(Nickel / Copper)": "30mm-airwrap-long-barrel-iron-copper",
    "New 30mm Airwrap™ long barrel(Nickel / Fuchsia)": "30mm-airwrap-long-barrel-iron-fuchsia",
    "New 20mm Airwrap™ barrel(Nickel / Iron)": "20mm-airwrap-barrel-iron-nickel",
    "New 20mm Airwrap™ barrel(Nickel / Copper)": "20mm-airwrap-barrel-iron-copper",
    "New 20mm Airwrap™ barrel(Nickel / Fuchsia)": "20mm-airwrap-barrel-iron-fuchsia",
    "New 40mm Airwrap™ barrel(Nickel / Iron)": "40mm-airwrap-barrel-iron-nickel",
    "New 40mm Airwrap™ barrel(Nickel / Copper)": "40mm-airwrap-barrel-iron-copper",
    "New 40mm Airwrap™ barrel(Nickel / Fuchsia)": "40mm-airwrap-barrel-iron-fuchsia",
    "New 30mm Airwrap™ barrel(Nickel / Iron)": "30mm-airwrap-barrel-iron-nickel",
    "New 30mm Airwrap™ barrel(Nickel / Copper)": "30mm-airwrap-barrel-iron-copper",
    "New 30mm Airwrap™ barrel(Nickel / Fuchsia)": "30mm-airwrap-barrel-iron-fuchsia",
}


def get_stock_list_for_table() -> list:
    stock_list_qs = Stock.objects.exclude(region="UK")
    stock_list_qs = (
        stock_list_qs.filter(name__startswith="New 20mm Airwrap")
        | stock_list_qs.filter(name__startswith="New 30mm Airwrap")
        | stock_list_qs.filter(name__startswith="New 40mm Airwrap")
        | stock_list_qs.filter(name__startswith="New Coanda")
        | stock_list_qs.filter(name__startswith="40mm Airwrap")
        | stock_list_qs.filter(name__startswith="30mm Airwrap")
        | stock_list_qs.filter(name__startswith="20mm Airwrap")
    )

    items = stock_list_qs.values_list(
        "region",
        "name",
        "stockdetail__color",
        "stockdetail__is_stock",
        "stockdetail__link",
        "stockdetail__modified_time",
    )
    return items


def send_mail(items):
    items = items.order_by("region")
    html = list_to_html(items)
    email = EmailMessage(
        f"Dyson 재고현황",  # 제목
        html,  # 내용
        to=["jhl0906@naver.com", "jarketss@gmail.com"],  # 받는 이메일 리스트
        # to=["jhl0906@naver.com"],  # 받는 이메일 리스트
    )
    email.content_subtype = "html"
    email.send()


def list_to_html(items: list) -> str:
    present_list = [
        ("New 40mm Airwrap™ long barrel", "롱40"),
        ("New 30mm Airwrap™ long barrel", "롱30"),
        ("New 20mm Airwrap™ barrel", "롱20"),
        ("New 40mm Airwrap™ barrel", "숏40"),
        ("New 30mm Airwrap™ barrel", "숏30"),
        ("New Coanda smoothing dryer", "코안다"),
        ("40mm Airwrap™ long barrel", "롱40(구)"),
        ("30mm Airwrap™ long barrel", "롱30(구)"),
        ("20mm Airwrap™ long barrel", "롱20(구)"),
        ("40mm Airwrap™ barrel", "숏40(구)"),
        ("30mm Airwrap™ barrel", "숏30(구)"),
    ]
    alist = []
    for key, value in present_list:
        fuchsia = ""
        iron = ""
        copper = ""
        purple = ""
        for item in items:
            if item[1] == key and item[2] == "Fuchsia" and item[3]:
                fuchsia += (
                    f'<a href="{item[4]}" target="_blank" style="color:blue">{item[0]}</a>\n'
                )
            elif (item[1] == key and item[2] == "Fuchsia") and not item[3]:
                fuchsia += (
                    f'<a href="{item[4]}" target="_blank" style="color:gray">{item[0]}</a>\n'
                )
            if item[1] == key and item[2] == "Iron" and item[3]:
                iron += f'<a href="{item[4]}" target="_blank" style="color:blue">{item[0]}</a>\n'
            elif (item[1] == key and item[2] == "Iron") and not item[3]:
                iron += f'<a href="{item[4]}" target="_blank" style="color:gray">{item[0]}</a>\n'
            if item[1] == key and item[2] == "Copper" and item[3]:
                copper += f'<a href="{item[4]}" target="_blank" style="color:blue">{item[0]}</a>\n'
            elif (item[1] == key and item[2] == "Copper") and not item[3]:
                copper += f'<a href="{item[4]}" target="_blank" style="color:gray">{item[0]}</a>\n'
            if item[1] == key and item[2] == "Purple" and item[3]:
                purple += f'<a href="{item[4]}" target="_blank" style="color:blue">{item[0]}</a>\n'
            elif (item[1] == key and item[2] == "Purple") and not item[3]:
                purple += f'<a href="{item[4]}" target="_blank" style="color:gray">{item[0]}</a>\n'

        alist.append(
            {
                "구분": value,
                "핑크": "·".join(fuchsia.split("\n")),
                "코퍼": "·".join(copper.split("\n")),
                "아이언": "·".join(iron.split("\n")),
                "퍼플": "·".join(purple.split("\n")),
            }
        )

    # 테이블 헤더 생성
    header = (
        "<tr style='border: 1px solid black;'>"
        + "".join([f"<th>{key}</th>" for key in alist[0].keys()])
        + "</tr>"
    )

    # 테이블 본문 생성
    rows = ""
    for row in alist:
        cells = "".join(
            [f"<td style='border: 1px solid black;'>{value}</td>" for value in row.values()]
        )
        rows += "<tr>" + cells + "</tr>"

    # 테이블 생성
    table = f"<table style='border: 1px solid black;'>{header}{rows}</table>"

    # 메일 전송 URL HTML 생성
    collected_html = "<li>현재까지 수집된 최신 정보를 메일로 받기: http://52.90.170.40:8000/api/v1/stocks/</li>"

    return table + collected_html


def crawler_dyson_stocks(region="UK"):
    # from stocks.models import Stock, StockDetail

    host = "www.dyson.co.uk"
    find_text = "Add to"
    if region == "UK":
        dyson_url = "https://www.dyson.co.uk/support/journey/tools/"
    elif region == "FR":
        dyson_url = "https://www.dyson.fr/support/journey/tools/"
        host = "www.dyson.fr"
        find_text = "Ajouter"
    elif region == "IT":
        dyson_url = "https://www.dyson.it/support/journey/tools/"
        host = "www.dyson.it"
        find_text = "Aggiungi"
    elif region == "DE":
        dyson_url = "https://www.dyson.de/support/journey/tools/"
        host = "www.dyson.de"
        find_text = "In den"
    elif region == "US":
        dyson_url = "https://www.dyson.com/support/journey/tools/"
        host = "www.dyson.com"
        find_text = "Add to"
    elif region == "JP":
        dyson_url = "https://www.dyson.co.jp/hair-care/haircare-accessories.aspx"
        host = "www.dyson.co.jp"
        find_text = "カートに入れる"
    elif region == "HK":
        dyson_url = "https://www.dyson.hk/zh-HK/"
        host = "www.dyson.hk"
        find_text = "加入購物車"
    elif region == "KR":
        dyson_url = "https://www.dyson.co.kr/"
        host = "www.dyson.co.kr"
        find_text = "장바구니 담기"
    elif region == "NL":
        dyson_url = "https://www.dyson.nl/haarstyling/multistyler/airwrap/accessoires/"
        host = "www.dyson.nl"
        find_text = "In winkelmand"
    elif region == "ES":
        dyson_url = "https://www.dyson.es/support/journey/tools/"
        host = "www.dyson.es"
        find_text = "Añadir a la cesta"
    elif region == "TR":
        dyson_url = "https://www.dyson.com.tr/"
        host = "www.dyson.com.tr"
        find_text = ""
    else:
        dyson_url = ""

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Host": host,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    item_numbers = {
        "New Coanda smoothing dryer(Nickel / Iron)": "971895-04",
        "New Coanda smoothing dryer(Nickel / Copper)": "971895-03",
        "New Coanda smoothing dryer(Nickel / Fuchsia)": "971895-01",
        "Wide-tooth comb(Nickel / Iron)": "971894-04",
        "Wide-tooth comb(Nickel / Copper)": "971894-03",
        "New 40mm Airwrap™ long barrel(Nickel / Iron)": "971889-08",
        "New 40mm Airwrap™ long barrel(Nickel / Copper)": "971889-07",
        "New 40mm Airwrap™ long barrel(Nickel / Fuchsia)": "971889-05",
        "40mm Airwrap™ long barrel(Nickel / Fuchsia)": "970290-01",  # 40mm 구형 롱배럴(핑크)
        "40mm Airwrap™ long barrel(Black / Purple)": "970290-02",  # 40mm 구형 롱배럴(퍼플)
        "New 30mm Airwrap™ long barrel(Nickel / Iron)": "971888-08",
        "New 30mm Airwrap™ long barrel(Nickel / Copper)": "971888-07",
        "New 30mm Airwrap™ long barrel(Nickel / Fuchsia)": "971888-05",
        "30mm Airwrap™ long barrel(Nickel / Fuchsia)": "970289-01",  # 30mm 구형 롱배럴(핑크)
        "30mm Airwrap™ long barrel(Black / Purple)": "970289-02",  # 30mm 구형 롱배럴(퍼플)
        "New 20mm Airwrap™ barrel(Nickel / Iron)": "971890-04",
        "New 20mm Airwrap™ barrel(Nickel / Copper)": "971890-03",
        "New 20mm Airwrap™ barrel(Nickel / Fuchsia)": "971890-01",
        "20mm Airwrap™ long barrel(Nickel / Fuchsia)": "970735-01",  # 20mm 구형 롱배럴(핑크)
        "20mm Airwrap™ long barrel(Black / Purple)": "970736-01",  # 20mm 구형 롱배럴(퍼플)
        "New 40mm Airwrap™ barrel(Nickel / Iron)": "971889-04",
        "New 40mm Airwrap™ barrel(Nickel / Copper)": "971889-03",
        "New 40mm Airwrap™ barrel(Nickel / Fuchsia)": "971889-01",
        "40mm Airwrap™ barrel(Nickel / Fuchsia)": "969470-01",  # 40mm 구형 숏배럴(핑크)
        "40mm Airwrap™ barrel(Black / Purple)": "969473-01",  # 40mm 구형 숏배럴(퍼플)
        "New 30mm Airwrap™ barrel(Nickel / Iron)": "971888-04",
        "New 30mm Airwrap™ barrel(Nickel / Copper)": "971888-03",
        "New 30mm Airwrap™ barrel(Nickel / Fuchsia)": "971888-01",
        "30mm Airwrap™ barrel(Nickel / Fuchsia)": "969466-01",  # 30mm 구형 숏배럴(핑크)
        "30mm Airwrap™ barrel(Black / Purple)": "969468-01",  # 30mm 구형 숏배럴(퍼플)
        "New Soft smoothing brush(Nickel / Iron)": "971891-08",
        "New Soft smoothing brush(Nickel / Copper)": "971891-07",
        "New Soft smoothing brush(Nickel / Fuchsia)": "971891-05",
        "New Firm smoothing brush": "971892-08",
        "Small soft smoothing brush(Nickel / Iron)": "971891-04",
        "Small soft smoothing brush(Nickel / Copper)": "971891-03",
        "Small soft smoothing brush(Nickel / Fuchsia)": "971891-01",
        "Small firm smoothing brush": "971892-04",
        "Round volumising brush(Nickel / Iron)": "971893-08",
        "Round volumising brush(Nickel / Copper)": "971893-07",
        "Round volumising brush(Nickel / Fuchsia)": "971893-05",
        "Small round volumising brush(Nickel / Iron)": "971893-04",
        "Small round volumising brush(Nickel / Copper)": "971893-03",
        "Small round volumising brush(Nickel / Fuchsia)": "971893-01",
        "upgrade kit: Complete long": "971874-17",
        "upgrade kit: Complete": "971874-16",
    }

    try:
        # 일본사이트는 페이지 구성이 다름..
        if region == "JP":
            response = requests.get(
                url=f"https://www.dyson.co.jp/api/ProductPricingAndAvailability?productIds=f6a67052-3345-4b26-ae6c-2d4174155c85&productIds=1c6b87ce-ad58-426b-a009-9dcb8cfce736&productIds=dbe1bc70-855f-45c7-ad2e-f39952ea1fdc&productIds=50f7d684-3fec-46fa-b31c-1e7e73be8274&productIds=cbd94a03-f90f-4313-9b37-2308cbeedcb1&productIds=0d2bb7e1-2d1a-4007-b5cc-42825d709219&productIds=652701e9-ef2d-43d1-843a-39583c95676b&productIds=6f670c53-ef52-4667-8f75-51711be0136d&productIds=3ba20954-0346-49e5-badf-9e71dfcebdec&productIds=fe45ef0d-37dc-4e71-93c1-7047bf686ee8&productIds=90ed2660-a27b-49fa-8ac2-447ddc6e93a0&productIds=1f00d107-299d-462b-8ceb-c2149128f882&productIds=4f3bf81c-3488-4fd2-b9bb-d047ecc3de6e&productIds=ab76d692-a16f-430d-9a11-bd24da1ab425&productIds=f69d6760-2900-4b5d-9583-1a4dacbe6d6e&productIds=d03ad326-bae1-4b65-a0cc-2ef41f0b632b&productIds=d1b74c61-d9f3-416b-ae82-d41438a49ab9&productIds=66ee4e40-cb9a-4be5-9f97-1db40cb25ce6&productIds=6ece57ed-eebb-43cc-b7b6-8f10d1d66ec9&productIds=ab82d6dd-698f-474e-a315-28564d2692cc&productIds=2762802d-b7ee-49e3-b0c1-9807b3536642&productIds=c010ede7-8c15-4635-a0e0-9ea3b387ad00&productIds=a0e5102e-fef1-44f5-a0a5-5bae9d70101e&productIds=845de55e-3ee9-4460-b68f-0a479e6e9181&productIds=82119cd5-044f-41bb-a125-979786a7645f&productIds=a38f437a-70df-4aa6-a7bf-e22762966cfb&productIds=ae37b1bd-4dcd-490b-9b8f-5712da8ff463&productIds=54ce91a2-095f-4103-8f35-5ad34cffe995&productIds=7c0f95f3-61d7-4e80-8321-5ae499c7f8b6&productIds=276d6d51-de7e-45d8-9128-3cbfa0349881&productIds=d708b394-e37f-410a-b5b2-7c4f32f62f4a&productIds=b3a21db3-78ef-402d-b16a-59ad32b9f305&productIds=0c6b2f11-ec34-440d-ad73-370c9a137160&productIds=297e3f62-afdd-48af-bd10-b965f412f26f",
                headers=headers,
            )

            time.sleep(3)
            stock_dict = {}
            for data in response.json():
                item_no = data.get("AvailabilityButton").get("AnalyticsLabel")[-9:]
                if data.get("AvailabilityButton").get("Text") == "カートに入れる":
                    stock_dict[item_no] = True
                else:
                    stock_dict[item_no] = False

            for name, number in item_numbers.items():
                if number in [
                    "970290-01",
                    "970290-02",
                    "970289-01",
                    "970289-02",
                    "970735-01",
                    "970736-01",
                    "969470-01",
                    "969473-01",
                    "969466-01",
                    "969468-01",
                ]:
                    continue

                if name.find("Iron") != -1:
                    color = "Iron"
                elif name.find("Copper") != -1:
                    color = "Copper"
                elif name.find("Fuchsia") != -1:
                    color = "Fuchsia"
                elif name.find("Purple") != -1:
                    color = "Purple"
                else:
                    color = None

                stock, created = Stock.objects.get_or_create(
                    name=name[: name.find("(")], region=region
                )

                # 해당 품번호의 재고 상태 확인
                try:
                    is_stock = stock_dict[number]
                except:
                    is_stock = False

                # 재고 상태 업데이트
                StockDetail.objects.update_or_create(
                    stock=stock,
                    color=color,
                    link=f"{dyson_url}",
                    defaults={"is_stock": True} if is_stock else {"is_stock": False},
                )
        elif region == "HK" or region == "KR":
            for name, product_name in DYSON_NAME.items():
                response = requests.get(url=f"{dyson_url}{product_name}", headers=headers)
                html_text = response.text

                text_index = html_text.find(find_text)

                if name.find("Iron") != -1:
                    color = "Iron"
                elif name.find("Copper") != -1:
                    color = "Copper"
                elif name.find("Fuchsia") != -1:
                    color = "Fuchsia"
                elif name.find("Purple") != -1:
                    color = "Purple"
                else:
                    color = None

                if name.find("(") != -1:
                    stock, created = Stock.objects.get_or_create(
                        name=name[: name.find("(")], region=region
                    )
                else:
                    stock, created = Stock.objects.get_or_create(name=name, region=region)

                if text_index != -1:
                    StockDetail.objects.update_or_create(
                        stock=stock,
                        color=color,
                        link=f"{dyson_url}{product_name}",
                        defaults={"is_stock": True},
                    )
                else:
                    StockDetail.objects.update_or_create(
                        stock=stock,
                        color=color,
                        link=f"{dyson_url}{product_name}",
                        defaults={"is_stock": False},
                    )
                time.sleep(3)

        else:
            for name, number in item_numbers.items():
                new_dyson_url = dyson_url
                new_number = number

                if number in [
                    "970290-01",
                    "970290-02",
                    "970289-01",
                    "970289-02",
                    "970735-01",
                    "970736-01",
                    "969470-01",
                    "969473-01",
                    "969466-01",
                    "969468-01",
                ] and region in ["NL"]:
                    continue

                # 독일, 스페인의 경우 URL 별도 처리
                if region == "DE":
                    if number in [
                        "970735-01",
                        "970736-01",
                        "969473-01",
                        "969468-01",
                    ]:
                        new_dyson_url = dyson_url[:-6]
                        new_number = f"spare-details.{number}"
                elif region == "ES":
                    if number in ["969473-01", "969468-01"]:
                        new_dyson_url = dyson_url[:-6]
                        new_number = f"spare-details.{number}"
                response = requests.get(url=f"{new_dyson_url}{new_number}", headers=headers)
                html_text = response.text

                # US의 경우 "You may also be interested in" 섹션이 존재하므로 제거
                if html_text.find("You may also") != -1:
                    html_text = html_text[: html_text.find("You may also")]

                text_index = html_text.find(find_text)

                if name.find("Iron") != -1:
                    color = "Iron"
                elif name.find("Copper") != -1:
                    color = "Copper"
                elif name.find("Fuchsia") != -1:
                    color = "Fuchsia"
                elif name.find("Purple") != -1:
                    color = "Purple"
                else:
                    color = None

                if name.find("(") != -1:
                    stock, created = Stock.objects.get_or_create(
                        name=name[: name.find("(")], region=region
                    )
                else:
                    stock, created = Stock.objects.get_or_create(name=name, region=region)

                if text_index != -1:
                    StockDetail.objects.update_or_create(
                        stock=stock,
                        color=color,
                        link=f"{dyson_url}{number}",
                        defaults={"is_stock": True},
                    )
                else:
                    StockDetail.objects.update_or_create(
                        stock=stock,
                        color=color,
                        link=f"{dyson_url}{number}",
                        defaults={"is_stock": False},
                    )
                time.sleep(3)
    except Exception as e:
        logger.exception(str(e), exc_info=e)
        pass
