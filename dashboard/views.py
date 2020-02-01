from django.shortcuts import render, redirect
from ssbear.util import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Order, Announcement, Bill, Node
from .models import TrafficLog
from account.models import InviteCode
from .forms import OrderForm, InviteForm, ChangeSSForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import update_session_auth_hash
import django.utils.timezone as timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta
import json


# Create your views here.
@login_required
def index(request):
    ann = Announcement.objects.last()
    orders = Order.objects.filter(user_id=request.user.id)[0:3]
    users = User.objects.filter(inviter_id=request.user.id)[0:3]
    invs = InviteCode.objects.filter(user_id=request.user.id).all()
    for inv in invs:
        inv.expired = inv.create_at + relativedelta(days=inv.days)
    return render(request, 'dashboard/index.html', locals())


@login_required
def info(request):
    users = User.objects.filter(inviter_id=request.user.id)[0:3]
    bills = Bill.objects.filter(user_id=request.user.id)[0:3]
    return render(request, 'dashboard/info.html', locals())


@login_required
def download(request):
    return render(request, 'dashboard/download.html', locals())


@login_required
def announcement_detail(request):
    announcement = Announcement.objects.all()
    return render(request, 'announcement/detail.html', locals())


@login_required
def buy(request):
    service_list = Service.objects.all()
    return render(request, 'dashboard/buy.html', locals())


@login_required
def confirm(request):
    sid = request.GET.get('sid', None)
    service = Service.objects.filter(id=sid).first()
    if not service:
        return HttpResponse("error", 404)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            remark = form.cleaned_data['remark']
            if not remark:
                remark = service.title
            password = form.cleaned_data['password']
            with transaction.atomic():
                if user.balance < service.price:
                    messages.warning(request, '余额不足，请充值')
                    return redirect('/dashboard/add_credit/')
                # use transaction to make the payment safe
                now = timezone.now()
                reset = now + relativedelta(months=1)
                expired = now + relativedelta(days=service.days)
                order = Order(
                    user_id=user.id,
                    service=service,
                    remark=remark,
                    port=Order.gen_port(),
                    uuid=Order.gen_uuid(),
                    password=password,
                    reset_at=reset,
                    expired_at=expired,
                    data_per_month=service.data_per_month,
                    price=service.price,
                    status=1,
                )
                order.save()

                bill = Bill(
                    user_id=user.id,
                    info=service.title,
                    info_cn=service.title_cn,
                    status=False,
                    payment=5,
                    price=service.price,
                    trade_no='order_' + str(order.id),
                )
                bill.save()
                # inviter gain benefit
                if user.inviter_id > 1:
                    bill2 = Bill(
                        user_id=user.inviter_id,
                        info="aff by " + user.email,
                        info_cn="通过邀请用户" + user.email + "获利",
                        status=True,
                        payment=1,
                        price=service.price / 10,
                        trade_no='aff_' + str(order.id),
                    )
                    bill2.save()
                    user2 = User.objects.filter(id=user.inviter_id).first()
                    user2.balance = user2.balance + service.price / 10
                    user2.save()

                user.balance = user.balance - service.price
                user.save()
                messages.success(request, '购买成功')
            return redirect('/dashboard/my_service/')
    else:
        form = OrderForm()
    return render(request, 'dashboard/confirm.html', locals())


@login_required
def pay(request):
    oid = request.GET.get('oid', None)
    order = Order.objects.filter(id=oid).first()
    if order.user_id != request.user.id:
        return redirect('/dashboard/')
    else:
        return render(request, 'dashboard/pay.html', locals())


@login_required
def my_service(request):
    orders = Order.objects.filter(user_id=request.user.id).all()
    return render(request, 'dashboard/my_service.html', locals())


@login_required
def invite_history(request):
    users = User.objects.filter(inviter_id=request.user.id).all()
    return render(request, 'dashboard/invite_history.html', locals())


@login_required
def add_credit(request):
    return HttpResponse("not ready yet")


@login_required
def add_invite(request):
    if not settings.INVITE_CODE:
        return HttpResponse("邀请功能暂时禁用", 403)

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            times = form.cleaned_data['times']
            text = form.cleaned_data['text']
            days = form.cleaned_data['days']
            inv = InviteCode.objects.filter(user_id=request.user.id).first()
            if inv:
                inv.text = text
                inv.times = times
                inv.days = days
                inv.save()
                messages.success(request, '邀请码更新成功')
                return redirect('/dashboard/')

            text = form.cleaned_data['text']
            invite = InviteCode.objects.filter(text=text).first()
            if invite:
                form.add_error('text', '换一个试试')
                return render(request, 'dashboard/add_invite.html', locals())
            else:
                newinv = InviteCode(
                    text=text,
                    times=times,
                    days=days,
                    user_id=request.user.id,
                )
                newinv.save()
                messages.success(request, '邀请码创建成功')
            return redirect('/dashboard/')
    else:
        form = InviteForm()
    return render(request, 'dashboard/add_invite.html', locals())


@login_required
def bill(request):
    bills = Bill.objects.filter(user_id=request.user.id).all()
    return render(request, 'dashboard/bill.html', locals())


@login_required
def order(request, id):
    try:
        order = Order.objects.get(pk=id)
    except:
        return HttpResponse('error', 404)
    if order.user_id != request.user.id:
        return redirect('/')
    tt = float(order.data_per_month * 1024 * 1024 * 1024)
    order.percent = round((order.traffic_up + order.traffic_down) * 100 / tt,
                          2)
    order.traffic_up = round(order.traffic_up / (1024 * 1024), 2)
    order.traffic_down = round(order.traffic_down / (1024 * 1024), 2)
    nodes = Node.objects.filter(is_public=True)
    for n in nodes:
        if n.mode == 1:
            n.qrcode = order.vmess_link(n)
        if n.mode == 0:
            n.qrcode = order.ss_link(n)
    return render(request, 'dashboard/order.html', locals())


@login_required
def change_ss_password(request, oid):
    try:
        order = Order.objects.get(id=oid)
    except:
        return HttpResponse('error', 404)

    if order.user_id != request.user.id:
        return HttpResponse("error", 404)

    if request.method == 'POST':
        form = ChangeSSForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            order.password = password
            order.save()
            messages.success(request, '密码已被修改')
            return redirect('/dashboard/order/' + str(order.id))
    else:
        form = ChangeSSForm()

    return render(request, 'dashboard/change_ss.html', locals())


@login_required
def change_uuid(request, oid):
    try:
        order = Order.objects.get(id=oid)
    except:
        return HttpResponse('error', 404)

    if order.user_id != request.user.id:
        return HttpResponse("error", 404)
    if request.method == 'POST':
        uuid = order.gen_uuid()
        order.uuid = uuid
        order.save()
        messages.success(request, 'UUID修改成功')
        return redirect('/dashboard/order/' + str(order.id))
    else:
        return render(request, 'dashboard/change_uuid.html', locals())


@login_required
def chart(request):
    oid = request.GET.get('oid', None)
    order = Order.objects.filter(id=oid).first()
    if not order:
        return HttpResponse("error", 404)
    if order.user_id != request.user.id:
        return HttpResponse("error", 404)

    traffics = TrafficLog.objects.filter(order_id=oid).all()
    dd = {}
    for t in traffics:
        k = str(t.create_at.date())
        if k not in dd.keys():
            dd[k] = t.traffic_down + t.traffic_up
        else:
            dd[k] += t.traffic_down + t.traffic_up
    resp = json.dumps(dd)

    return render(request, 'dashboard/chart.html', locals())
