# ssbear



```
+----------+            +-------------+        +--------------+
|          |            |             |        |              |
|  ssbear  +------------+   syncbear  +--------+  shadowsocks |
|          |            |             |        |              |
+-----+----+            +-------------+        +--------------+
      |
      |                 +-------------+        +--------------+
      |                 |             |        |              |
      +-----------------+   syncbear  +--------+    v2ray     |
                        |             |        |              |
                        +-------------+        +--------------+
```



## install

pip install django==2.2.9

pip install python-dateutil

pip install django-anymail[mailgun]

pip install django-crontab

pip install psycopg2

pip install python-alipay-sdk

#### how to use crontab

python manage.py crontab add

python manage.py crontab show

python manage.py crontab remove



## todo

- [ ] Save traffic to redis and show it in graphic 
- [x] useful front page
- [x] add alipay
- [x] restructure v2ray sidecar
- [x] add support to ss
- [ ] add support to trojan
- [x] make dashboard support mobile
- [x] make interface simple , no need to support mobile
- [x] recode invite code
- [x] remove i18n



# debug email

python -m smtpd -n -c DebuggingServer localhost:1025



## links

https://github.com/fzlee/alipay

