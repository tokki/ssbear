from django.contrib import admin

from .models import Service, Order,Announcement,Bill,Node
from .models import TrafficLog
# Register your models here.

admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Bill)
admin.site.register(Node)
admin.site.register(Announcement)
admin.site.register(TrafficLog)
