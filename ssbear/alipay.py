import os
from alipay import AliPay

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

alipay_public = open(os.path.join(BASE_DIR,'ssbear/key/ali_public_key.pem')).read()
app_private = open(os.path.join(BASE_DIR,'ssbear/key/app_private_key.pem')).read()

def alipay(): 
    pay = AliPay( 
        appid='2016101800714233',
        app_notify_url= settings.SITE_URL+'/api/alipay/',
        app_private_key_string= app_private,
        alipay_public_key_string= alipay_public,
        sign_type="RSA",
        debug=False,
    )
    return pay
