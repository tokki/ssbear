from django import forms
from .models import InviteCode


class EmailForm(forms.Form):
    email = forms.CharField(
        label='邮箱',
        error_messages={
            'required': '不能为空',
            'invalid': '邮箱格式错误',
        },
    )


class RegisterForm(forms.Form):
    invite = forms.CharField(
        label='邀请码',
        error_messages={
            'required': '不能为空',
        },
    )
    username = forms.SlugField(
        label='用户名',
        error_messages={
            'required': '不能为空',
            'invalid': '只能包含a-zA-Z-_',
        },
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'required': '不能为空',
            'invalid': '邮箱格式错误',
        },
    )
    password = forms.CharField(
        label='密码',
        max_length=32,
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(),
        error_messages={
            'required': '不能为空',
        },
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )


class SendCodeForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={
            'placeholder': 'your@email.com',
        }),
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
        },
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={
            'placeholder': 'your@mail.com',
        }),
        error_messages={
            'required': '不能为空',
            'invalid': '邮箱格式错误',
        },
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        error_messages={
            'required': '不能为空',
        },
    )
    new = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )
    new2 = forms.CharField(
        label='再次输入',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )


class ChangePasswordForm(forms.Form):
    old = forms.CharField(
        label='旧密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )
    new = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )
    new2 = forms.CharField(
        label='再次输入',
        widget=forms.PasswordInput,
        error_messages={
            'required': '不能为空',
        },
    )
