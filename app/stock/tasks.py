import threading
from django.core.mail import EmailMessage
from background_task import background
from django.db import transaction
from stock.manager import crawler_dyson_stocks
from stock.manager import list_to_html, get_stock_list_for_table


@background(schedule=30)
def task_send_mail():
    items = get_stock_list_for_table()
    items = items.order_by("region")
    html = list_to_html(items)
    email = EmailMessage(
        f"Dyson 재고현황",  # 제목
        html,  # 내용
        to=["jhl0906@naver.com", "jarketss@gmail.com"],  # 받는 이메일 리스트
    )
    email.content_subtype = "html"
    email.send()


@background(schedule=30)
def task_crawler_dyson():
    threads = []
    with transaction.atomic():
        # for region in ["DE", "IT", "FR", "US", "JP", "HK", "KR", "NL", "ES"]:
        for region in ["DE", "IT", "FR", "US", "JP", "NL", "ES"]:
            t = threading.Thread(target=crawler_dyson_stocks, args=(region,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
