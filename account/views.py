from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from .models import InviteCode
from .models import ResetCode
from .forms import RegisterForm, LoginForm, ChangePasswordForm, SendCodeForm
from .forms import ResetPasswordForm, EmailForm
from .forms import ChangePasswordForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from ssbear.mail import send_code
from django.utils import timezone
from datetime import timedelta
from ssbear.util import render
from django.views import View

class Home(View):
    def get(self, request):
        return render(request, 'index.html', locals())

class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', locals())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user:
                messages.success(request, '登录成功')
                login(request, user)
                return redirect('/dashboard/')
            else:
                form.add_error('username', '用户名或密码错误')
        return render(request, 'account/login.html', locals())


class SendCode(View):
    def get(self, request):
        form = SendCodeForm()
        return render(request, 'account/send_code.html', locals())

    def post(self, request):
        if request.method == 'POST':
            form = SendCodeForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = User.objects.filter(email=email).first()
                if user:
                    res = ResetCode.objects.filter(email=email).first()
                    if res:
                        timezone.now() < res.create_at + timedelta(minutes=60)
                        form.add_error('email', '过一会再试试')
                    else:
                        send_code(user)
                        messages.success(request, '发送成功，注意查看邮箱')
                        return redirect('/account/reset_password/?q=' + email)
                else:
                    form.add_error('email', '过一会再试试')
        return render(request, 'account/send_code.html', locals())


class ResetPassword(View):
    def get(self, request):
        email = request.GET.get('q')
        form = ResetPasswordForm(initial={'email': email})
        return render(request, 'account/reset_password.html', locals())

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            new = form.cleaned_data['new']
            new2 = form.cleaned_data['new2']
            if new != new2:
                form.add_error('new2', '两次输入的不一致')
                return render(request, 'account/reset_password.html', locals())
            else:
                res = ResetCode.objects.filter(email=email).first()
                if res and res.code == code:
                    user = User.objects.filter(email=email).first()
                    user.set_password(new)
                    user.save()
                    messages.success(request, '密码修改成功')
                    return redirect('/account/login/')
                else:
                    form.add_error('code', '验证码错误')
            return render(request, 'account/reset_password.html', locals())


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/account/login/')


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', locals())

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            invite = form.cleaned_data['invite']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            inv = InviteCode.objects.filter(text=invite).first()
            if not inv:
                form.add_error('invite', '邀请码错误')
                return render(request, 'account/register.html', locals())
            else:
                expired = timezone.now() > inv.create_at + timedelta(
                    days=inv.days)
                if expired or inv.times < 1:
                    form.add_error('invite', '邀请码错误')
                    return render(request, 'account/register.html', locals())
                u = User.objects.filter(username=username).first()
                if u:
                    form.add_error('username', '用户名已存在')
                    return render(request, 'account/register.html', locals())
                else:
                    newuser = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    newuser.inviter_id = inv.user_id
                    newuser.save()
                    inv.times = inv.times - 1
                    inv.save()
                    messages.success(request, '登录成功')
                    login(request, newuser)
                    return redirect('/dashboard/')
        return render(request, 'account/register.html', locals())


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'account/change_password.html', locals())

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old = form.cleaned_data['old']
            new = form.cleaned_data['new']
            new2 = form.cleaned_data['new2']
            user = authenticate(
                request,
                username=request.user.username,
                password=old,
            )
            if user:
                if new != new2:
                    form.add_error('new2', '两次输入的不一致')
                else:
                    user.set_password(new)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '密码修改成功')
                    return redirect('/dashboard/')
            else:
                form.add_error('old', '旧密码错误')

        return render(request, 'account/change_password.html', locals())


class ChangeEmail(LoginRequiredMixin, View):
    def get(self, request):
        form = EmailForm()
        return render(request, 'account/change_email.html', locals())

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            u = User.objects.filter(id=request.user.id).first()
            u.email = email
            u.save()
            messages.success(request, '邮箱修改成功')
            return redirect('/dashboard/')
        return render(request, 'account/change_email.html', locals())

