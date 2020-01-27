from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Service, Order


class OrderForm(forms.Form):
    remark = forms.CharField(
        label=_('Remark'),
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    password = forms.CharField(
        label=_('Shadowsocks password'),
        error_messages={
            'required': _('Please file out this field'),
        },
    )


class ChangeSSForm(forms.Form):
    password = forms.CharField(
        label=_('Password'),
        error_messages={
            'required': _('Please file out this field'),
        },
    )


class InviteForm(forms.Form):
    text = forms.SlugField(
        label=_('Text'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Text only contains letter number _-'),
        },
    )
    times = forms.IntegerField(
        label=_('Times'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Number format error'),
        },
    )
    days = forms.IntegerField(
        label=_('During days'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Number format error'),
        },
    )
