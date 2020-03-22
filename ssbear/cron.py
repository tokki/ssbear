from dashboard.models import Order,TrafficLog
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db import transaction


@transaction.atomic
def reset_data():
    orders = Order.objects.all()
    for order in orders:
        diff = order.reset_at - timezone.now()
        if diff.days == 0:
            order.traffic_down = 0
            order.traffic_up = 0
            order.status = 1
            if timezone.now() <= order.expired_at:
                new_reset = order.reset_at + relativedelta(months=1)
                order.reset_at = new_reset
            else:
                order.status = 0
            order.save()

@transaction.atomic
def clean_traffic_log():
    traffics = TrafficLog.objects.all()
    for traffic in traffics:
        diff = timezone.now() - traffic.create_at 
        if diff.days > 20:
            print(diff)
            traffic.delete()
