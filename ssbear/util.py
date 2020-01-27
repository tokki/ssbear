from django.shortcuts import render as render_tpl
from django.conf import settings
from functools import wraps
from django.http import JsonResponse


def render(request, tpl, content):
    content['settings'] = settings
    return render_tpl(request, tpl, content)


def api_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("token", "")
        if token != settings.API_TOKEN:
            return JsonResponse({"msg": "token is missing"},status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
