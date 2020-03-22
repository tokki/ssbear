from django.views.decorators.csrf import csrf_exempt
from ssbear.util import api_auth
from django.contrib.auth import get_user_model
User = get_user_model()
from dashboard.models import Order, TrafficLog,Bill,AlipayOrder
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
from ssbear.alipay import alipay
import json


@csrf_exempt
@transaction.atomic
def alipay_callback(request):
    if request.method == 'POST':
        data = request.POST.dict()
        signature = data['sign']
        pay = alipay()
        try:
            success = pay.verify(data, signature)
        except:
            success = False
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
            oid = int(data['out_trade_no'].replace('ssbear_',''))
            order = AlipayOrder.objects.filter(id=oid).first()
            if order and order.status == 0:
                order.status = 1
                trade_no = data['trade_no']
                order.save()

                user = User.objects.filter(id=order.user_id).first()
                user.balance = user.balance + order.amount
                user.save()

                bill = Bill(
                    user_id = order.user_id,
                    info = '支付宝充值',
                    status = True,
                    payment = 0,
                    price = order.amount,
                    trade_no ='alipay_'+str(order.id),
                )
                bill.save()
            return HttpResponse(status=204)
        

@api_auth
@csrf_exempt
def sync(request):
    order_list = Order.objects.filter(status=1)
    data = {o.id: o.uuid for o in order_list}
    return JsonResponse(data)


@api_auth
@csrf_exempt
def sync_ss(request):
    order_list = Order.objects.filter(status=1)
    data = {o.port: o.password for o in order_list}
    return JsonResponse(data)


@api_auth
@csrf_exempt
@transaction.atomic
def traffic_ss(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = None
        if data:
            port_list = []
            for k, v in data.items():
                port_list.append(int(k))
            orders = Order.objects.filter(port__in=port_list)
            for order in orders:
                order.traffic_down += int(data[order.port])
                dd = order.data_per_month * 1024 * 1024 * 1024
                if order.traffic_up + order.traffic_down > dd:
                    # disable empty data orders
                    order.status = 0
            Order.objects.bulk_update(orders, [
                'traffic_down',
                'status',
            ])


@api_auth
@csrf_exempt
@transaction.atomic
def traffic(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = None
        if data:
            id_list = []
            for k, v in data.items():
                dd = k.split("@")
                if int(dd[0]) not in id_list:
                    id_list.append(int(dd[0]))
            orders = Order.objects.filter(id__in=id_list)

            for order in orders:
                order.traffic_up += data[str(order.id) + "@uplink"]
                order.traffic_down += data[str(order.id) + "@downlink"]
                dd = order.data_per_month * 1024 * 1024 * 1024
                if order.traffic_up + order.traffic_down > dd:
                    # disable empty data orders
                    order.status = 0
            Order.objects.bulk_update(orders, [
                'traffic_up',
                'traffic_down',
                'status',
            ])

            tlog = []
            for order in orders:
                tup = data[str(order.id)+"@uplink"]
                tdown= data[str(order.id)+"@downlink"]
                if tdown > 0:
                    newlog = TrafficLog(
                        order_id = order.id,
                        traffic_up = tup,
                        traffic_down = tdown,
                    )
                    tlog.append(newlog)
            if len(tlog) > 0:
                TrafficLog.objects.bulk_create(tlog)
        return HttpResponse(status=204)

