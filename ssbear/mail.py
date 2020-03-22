from django.core.mail import send_mail
import random
from account.models import ResetCode

# Create your views here.


def send_code(user):
    code = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 5))
    msg = '''
    重置密码的验证码是: ''' + code + '''。

    如果仍然有问题，请邮件管理员。

    '''
    res = ResetCode.objects.filter(email=user.email).first()
    if res:
        res.delete()
    rc = ResetCode(email=user.email,code=code)
    rc.save()
    send_mail( "重置密码--ssbear.com", msg, "ssbear <noreply@ssbear.com>", [user.email],)
    #print(code+msg)

    
