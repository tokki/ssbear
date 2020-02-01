from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import InviteCode
from .models import ResetCode
from .forms import RegisterForm, LoginForm, ChangePasswordForm, SendCodeForm
from .forms import ResetPasswordForm,EmailForm
from .forms import ChangePasswordForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from ssbear.mail import send_code
from django.utils import timezone
from datetime import timedelta
from ssbear.util import render


def index(request):
    return render(request, 'index.html', locals())


def set_language(request):
    lang = request.GET.get('lang', None)
    path = request.GET.get('next', None)
    if path:
        response = redirect(path)
    else:
        response = redirect('/')
    if lang == 'zh-hans':
        response.set_cookie('django_language', 'zh-hans')
    else:
        response.set_cookie('django_language', 'en-us')
    return response


def login_view(request):
    if request.method == 'POST':
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
                messages.success(request, _('Login Success'))
                login(request, user)
                return redirect('/dashboard/')
            else:
                form.add_error('username', _('account or password error'))
    else:
        form = LoginForm()
    return render(request, 'account/login.html', locals())


def send_code_view(request):
    if request.method == 'POST':
        form = SendCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                res = ResetCode.objects.filter(email=email).first()
                if res:
                    timezone.now() < res.create_at + timedelta(minutes=60)
                    form.add_error('email', _('Please try later'))
                else:
                    send_code(user)
                    messages.success(request,
                                     _('Send success, plz check your email'))
                    return redirect('/account/reset_password/?q=' + email)
            else:
                form.add_error('email', _('Please try later'))
    else:
        form = SendCodeForm()
    return render(request, 'account/send_code.html', locals())


def reset_password_view(request):
    if request.POST:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            new = form.cleaned_data['new']
            new2 = form.cleaned_data['new2']
            if new != new2:
                form.add_error('new2', _('Not the same password your input'))
                return render(request, 'account/reset_password.html', locals())
            else:
                res = ResetCode.objects.filter(email=email).first()
                if res and res.code == code:
                    user = User.objects.filter(email=email).first()
                    user.set_password(new)
                    user.save()
                    messages.success(request, _('Password change success'))
                    return redirect('/account/login/')
                else:
                    form.add_error('code', _('Reset code error'))
    else:
        email = request.GET.get('q')
        form = ResetPasswordForm(initial={'email': email})
    return render(request, 'account/reset_password.html', locals())


def logout_view(request):
    logout(request)
    return redirect('/account/login/')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            invite = form.cleaned_data['invite']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            inv = InviteCode.objects.filter(text=invite).first()
            if not inv:
                form.add_error('invite', _('Invite code error'))
                return render(request, 'account/register.html', locals())
            else:
                expired = timezone.now() > inv.create_at + timedelta(
                    days=inv.days)
                if expired or inv.times < 1:
                    form.add_error('invite', _('Invite code error'))
                    return render(request, 'account/register.html', locals())
                u = User.objects.filter(username=username).first()
                if u:
                    form.add_error('username', _('Account name already exist'))
                    return render(request, 'account/register.html', locals())
                else:
                    newuser = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    newuser.inviter_id = inv.user_id
                    if inv.text == 'bwave':
                        newuser.balance = 120.00
                    newuser.save()
                    inv.times = inv.times - 1
                    inv.save()
                    messages.success(request, _('Login success'))
                    login(request, newuser)
                    return redirect('/dashboard/')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', locals())


@login_required
def change_password_view(request):
    if request.method == 'POST':
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
                    form.add_error('new2',
                                   _('Not the same password your input'))
                else:
                    user.set_password(new)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, _('Password has been changed'))
                    return redirect('/dashboard/')
            else:
                form.add_error('old', _('Password error'))
    else:
        form = ChangePasswordForm()

    return render(request, 'account/change_password.html', locals())


@login_required
def change_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            u = User.objects.filter(id=request.user.id).first()
            u.email = email
            u.save()
            messages.success(request, _('Email has been changed'))
    else:
        form = EmailForm()
    return render(request, 'account/change_email.html', locals())
