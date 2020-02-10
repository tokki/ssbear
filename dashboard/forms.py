from django import forms
from .models import Service, Order


class OrderForm(forms.Form):
    remark = forms.CharField(
        label='备注名',
        error_messages={
            'required': '不能为空',
        },
    )
    password = forms.CharField(
        label='Shadowsocks密码',
        error_messages={
            'required': '不能为空',
        },
    )


class ChangeSSForm(forms.Form):
    password = forms.CharField(
        label='密码',
        error_messages={
            'required': '不能为空',
        },
    )


class InviteForm(forms.Form):
    text = forms.SlugField(
        label='字符',
        error_messages={
            'required': '不能为空',
            'invalid': '字符只能包含a-z A-Z _ - ',
        },
    )
    times = forms.IntegerField(
        label='次数',
        error_messages={
            'required': '不能为空',
            'invalid': '只可以是数字',
        },
    )
    days = forms.IntegerField(
        label='有效天数',
        error_messages={
            'required': '不能为空',
            'invalid': '只可以是数字',
        },
    )


class CodepayForm(forms.Form):
    text = forms.SlugField(
        label='字符',
        error_messages={
            'required': '不能为空',
            'invalid': '字符只能包含a-z A-Z _ - ',
        },
    )


class AlipayForm(forms.Form):
    amount = forms.IntegerField(
        label='金额/元',
        error_messages={
            'required': '不能为空',
            'invalid': '只能是整数',
        },
    )
