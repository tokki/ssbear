import json
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class JsonLoginRequiredMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        data = {'msg': 'unauthorized'}
        if not request.user.is_authenticated:
            return JsonResponse(data, status=403)
        return super(JsonLoginRequiredMixin,
                     self).dispatch(request, *args, **kwargs)
