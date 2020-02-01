from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import django.utils.timezone as timezone
import datetime, time
import random
import base64
import json
import uuid
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=40)
    title_cn = models.CharField(max_length=40)
    content = models.TextField()
    content_cn = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ("-create_at", )

    def __str__(self):
        return self.title


class Node(models.Model):
    MODE = [
        (0, _('Shadowsocks')),
        (1, _('V2ray')),
    ]
    name = models.CharField(max_length=40)
    name_cn = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    description_cn = models.CharField(max_length=40)
    host = models.CharField(max_length=40)
    mode = models.IntegerField(default=0, choices=MODE)
    create_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ("-create_at", )

    def __str__(self):
        return self.name


class Bill(models.Model):
    PAYMENT = (
        (0, _('alipay face to face')),
        (1, _('aff from user')),
        (5, _('buy service')),
    )
    user_id = models.IntegerField(default=0)
    info = models.CharField(max_length=40)
    info_cn = models.CharField(max_length=40)
    # status for bill true == add false == use
    status = models.BooleanField()
    payment = models.IntegerField(default=0, choices=PAYMENT)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    trade_no = models.CharField(max_length=100)

    class Meta:
        ordering = ("-create_at", )

    def __str__(self):
        return self.trade_no

    @classmethod
    def gen_trade_no(cls):
        return datetime.datetime.fromtimestamp(
            time.time()).strftime("%Y%m%d%H%M%S%s")


class Service(models.Model):
    title = models.CharField(max_length=40)
    title_cn = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    description_cn = models.CharField(max_length=300)
    data_per_month = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS = [
        (0, _('disable')),
        (1, _('enable')),
    ]
    user_id = models.IntegerField(default=0)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    remark = models.CharField(max_length=40)
    port = models.CharField(max_length=5, default="")
    uuid = models.CharField(max_length=36)
    password = models.CharField(max_length=40)
    create_at = models.DateTimeField(auto_now_add=True)
    reset_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    method = models.CharField(max_length=40, default="rc4-md5")
    data_per_month = models.IntegerField(default=0)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
    )

    status = models.IntegerField(default=0, choices=STATUS)
    traffic_up = models.BigIntegerField(default=0)
    traffic_down = models.BigIntegerField(default=0)

    class Meta:
        ordering = ("-create_at", )

    def __str__(self):
        return self.remark

    @classmethod
    def gen_port(cls):
        order = cls.objects.all()
        used_port = [o.port for o in order]
        ports = []
        for i in range(10000, 30000):
            if str(i) not in used_port:
                ports.append(str(i))

        return random.choice(ports)

    @classmethod
    def gen_uuid(cls):
        return uuid.uuid4()

    def ss_link(cls, node):
        s = f"{self.method}:{self.passowrd}@{node.host}:{self.port}"
        v = f"ss://{base64.urlsafe_b64encode(s.encode()).decode()}"
        return uuid.uuid4()

    def vmess_link(self, node):
        obj = {
            'v': '2',
            'ps': node.name,
            'add': node.host,
            'port': '443',
            'id': self.uuid,
            'aid': '30',
            'net': 'ws',
            'type': 'none',
            'host': node.host,
            'path': '/ssbear',
            'tls': 'tls',
        }
        tpl = json.dumps(obj)
        v = f"vmess://{base64.urlsafe_b64encode(tpl.encode()).decode()}"
        return v


class TrafficLog(models.Model):
    order_id = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True, db_index=True)
    traffic_up = models.BigIntegerField(_("Upload traffic"), default=0)
    traffic_down = models.BigIntegerField(_("download Traffic"), default=0)

    def __str__(self):
        return str(self.create_at)
