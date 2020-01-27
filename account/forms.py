from django import forms
from django.utils.translation import gettext_lazy as _
from .models import InviteCode


class EmailForm(forms.Form):
    email = forms.CharField(
        label=_('Email'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Email format error'),
        },
    )


class RegisterForm(forms.Form):
    invite = forms.CharField(
        label=_('Invite Code'),
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    username = forms.SlugField(
        label=_('Account Name'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Account name must be "a-zA-Z-_"'),
        },
    )
    email = forms.EmailField(
        label=_('Email'),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Email format error'),
        },
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=32,
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Account name'),
        widget=forms.TextInput(),
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )


class SendCodeForm(forms.Form):
    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(attrs={
            'placeholder': 'your@email.com',
        }),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Email format error'),
        },
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs={
            'placeholder': 'your@mail.com',
        }),
        error_messages={
            'required': _('Please file out this field'),
            'invalid': _('Email format error'),
        },
    )

    code = forms.CharField(
        label=_('Reset Code'),
        widget=forms.TextInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    new = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    new2 = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )


class ChangePasswordForm(forms.Form):
    old = forms.CharField(
        label=_('Old password'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    new = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )
    new2 = forms.CharField(
        label=_('Password again'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please file out this field'),
        },
    )
