import os
from alipay import AliPay

from django.conf import settings


alipay_public_key_string = open("key/alipay_pub.pem").read()
app_private_key_string = open("key/app_pravite.pem").read()


pay = Alipayments(APPID, PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)

alipay = AliPay(
    appid="",
    app_notify_url= settings.SITE_URL+'/api/alipay/'  # the default notify path
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
    debug=False  # False by default
)
