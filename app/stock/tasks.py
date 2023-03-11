from background_task import background
from django.contrib.auth.models import User
import threading

from django.db import transaction
from stock.manager import crawler_dyson_stocks

@background(schedule=30)
def add_task_queue():
    # if TaskQueue.objects.filter(status="PROCESS"):
    #     return

    threads = []
    with transaction.atomic():
        # try:
        #     instance = TaskQueue.objects.get(status="READY")
        # except TaskQueue.DoesNotExist:
        #     return
        #
        # if TaskQueue.objects.filter(status="PROCESS").exists():
        #     return
        # instance.status = "PROCESS"
        # instance.save()
        for region in ["DE", "IT", "FR", "US", "JP", "HK", "KR", "NL", "ES"]:
        # for region in ["NL", "ES"]:
            t = threading.Thread(target=crawler_dyson_stocks, args=(region,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    # TaskQueue.objects.update(status="SUCCESS")
    # items = get_stock_list_for_table()
    # send_mail2(items)
