from django.shortcuts import render, redirect
from ssbear.util import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Order, Announcement, Bill, Node
from .models import TrafficLog, Codepay, AlipayOrder
from account.models import InviteCode
from .forms import OrderForm, InviteForm, ChangeSSForm, CodepayForm
from .forms import AlipayForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import django.utils.timezone as timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta
import json
from ssbear.alipay import alipay


# Create your views here.
class Index(LoginRequiredMixin, View):
    def get(self, request):
        ann = Announcement.objects.last()
        orders = Order.objects.filter(user_id=request.user.id)[0:3]
        users = User.objects.filter(inviter_id=request.user.id)[0:3]
        invs = InviteCode.objects.filter(user_id=request.user.id).all()
        for inv in invs:
            inv.expired = inv.create_at + relativedelta(days=inv.days)
        return render(request, 'dashboard/index.html', locals())


class Info(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(inviter_id=request.user.id)[0:3]
        bills = Bill.objects.filter(user_id=request.user.id)[0:3]
        return render(request, 'dashboard/info.html', locals())


class Download(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/download.html', locals())


class AnnouncementDetail(LoginRequiredMixin, View):
    def get(self, request):
        announcement = Announcement.objects.all()
        return render(request, 'announcement/detail.html', locals())


class Buy(LoginRequiredMixin, View):
    def get(self, request):
        service_list = Service.objects.all()
        return render(request, 'dashboard/buy.html', locals())


class Confirm(LoginRequiredMixin, View):
    def get(self, request):
        sid = request.GET.get('sid', None)
        service = Service.objects.filter(id=sid).first()
        if not service:
            return HttpResponse("error", 404)
        form = OrderForm()
        return render(request, 'dashboard/confirm.html', locals())

    @transaction.atomic
    def post(self, request):
        sid = request.GET.get('sid', None)
        service = Service.objects.filter(id=sid).first()
        if not service:
            return HttpResponse("error", 404)

        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            remark = form.cleaned_data['remark']
            if not remark:
                remark = service.title
            password = form.cleaned_data['password']
            if user.balance < service.price:
                messages.warning(request, '余额不足，请充值')
                return redirect('/dashboard/add_credit/')
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
                info="购买套餐" + service.title,
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
                    info="通过邀请用户" + user.email + "获利",
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
        return render(request, 'dashboard/confirm.html', locals())


class Pay(LoginRequiredMixin, View):
    def get(self, request):
        bills = Bill.objects.filter(user_id=request.user.id)[0:3]
        return render(request, 'dashboard/pay.html', locals())


class AlipayPage(LoginRequiredMixin, View):
    def get(self, request):
        if not settings.ALIPAY:
            return HttpResponse('disabled', status=403)
        form = AlipayForm()
        return render(request, 'dashboard/alipay_page.html', locals())

    def post(self, request):
        if not settings.ALIPAY:
            return HttpResponse('disabled', status=403)

        form = AlipayForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            ali_order = AlipayOrder(
                user_id=request.user.id,
                info="充值",
                amount=amount,
                trade_no="",
            )
            ali_order.save()

            pay = alipay()
            subject = settings.SITE_NAME + "支付订单"

            order_string = pay.api_alipay_trade_page_pay(
                out_trade_no=ali_order.out_trade_no,
                total_amount=amount,
                subject=subject,
                return_url=settings.SITE_URL + "/dashboard/pay/",
            )
            getway = "https://openapi.alipay.com/gateway.do?" + order_string
            return redirect(getway)
        return render(request, 'dashboard/alipay_page.html', locals())


class Codepay(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = CodepayForm()
        return render(request, 'dashboard/codepay.html', locals())

    @transaction.atomic
    def post(self, request):
        form = CodepayForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            code = Codepay.objects.filter(text=text).first()
            if not code or code.status == 0:
                form.add_error('text', '充值码输入错误')
                return render(request, 'dashboard/codepay.html', locals())
            else:
                user.balance = user.balance + code.balance
                user.save()
                code.status = 0
                code.save()
                bill = Bill(
                    user_id=user.id,
                    info='通过充值码充值',
                    status=True,
                    payment=2,
                    price=code.balance,
                    trade_no='code_' + str(code.id),
                )
                bill.save()
            messages.success(request, '充值成功')
            return redirect('/dashboard/pay/')
        return render(request, 'dashboard/codepay.html', locals())


class MyService(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id).all()
        return render(request, 'dashboard/my_service.html', locals())


class InviteHistory(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(inviter_id=request.user.id).all()
        return render(request, 'dashboard/invite_history.html', locals())


class AddInvite(LoginRequiredMixin, View):
    def get(self, request):
        if not settings.INVITE_CODE:
            return HttpResponse('disabled', status=403)
        form = InviteForm()
        return render(request, 'dashboard/add_invite.html', locals())

    def post(self, request):
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
        return render(request, 'dashboard/add_invite.html', locals())


class BillInfo(LoginRequiredMixin, View):
    def get(self, request):
        bills = Bill.objects.filter(user_id=request.user.id).all()
        return render(request, 'dashboard/bill.html', locals())


class OrderInfo(LoginRequiredMixin, View):
    def get(self, request, oid):
        try:
            order = Order.objects.get(pk=oid)
        except:
            return HttpResponse('error', 404)
        if order.user_id != request.user.id:
            return redirect('/')
        tt = float(order.data_per_month * 1024 * 1024 * 1024)
        order.percent = round(
            (order.traffic_up + order.traffic_down) * 100 / tt, 2)
        order.traffic_up = round(order.traffic_up / (1024 * 1024), 2)
        order.traffic_down = round(order.traffic_down / (1024 * 1024), 2)
        nodes = Node.objects.filter(is_public=True)
        for n in nodes:
            if n.mode == 1:
                n.qrcode = order.vmess_link(n)
            if n.mode == 0:
                n.qrcode = order.ss_link(n)
        return render(request, 'dashboard/order.html', locals())


class SSPassword(LoginRequiredMixin, View):
    def get(self, request, oid):
        try:
            order = Order.objects.get(id=oid)
        except:
            return HttpResponse('error', 404)
        if order.user_id != request.user.id:
            return HttpResponse("error", 404)
        form = ChangeSSForm()
        return render(request, 'dashboard/change_ss.html', locals())

    def post(self, request, oid):
        try:
            order = Order.objects.get(id=oid)
        except:
            return HttpResponse('error', 404)
        if order.user_id != request.user.id:
            return HttpResponse("error", 404)

        form = ChangeSSForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            order.password = password
            order.save()
            messages.success(request, '密码已被修改')
            return redirect('/dashboard/order/' + str(order.id))
        return render(request, 'dashboard/change_ss.html', locals())


class V2rayPassword(LoginRequiredMixin, View):
    def get(self, request, oid):
        try:
            order = Order.objects.get(id=oid)
        except:
            return HttpResponse('error', 404)
        if order.user_id != request.user.id:
            return HttpResponse("error", 404)
        return render(request, 'dashboard/change_uuid.html', locals())

    def post(self, request, oid):
        try:
            order = Order.objects.get(id=oid)
        except:
            return HttpResponse('error', 404)
        if order.user_id != request.user.id:
            return HttpResponse("error", 404)
        uuid = order.gen_uuid()
        order.uuid = uuid
        order.save()
        messages.success(request, 'UUID修改成功')
        return redirect('/dashboard/order/' + str(order.id))


class Chart(LoginRequiredMixin, View):
    def get(self, request):
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
