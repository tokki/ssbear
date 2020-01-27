# ssbear

python -m smtpd -n -c DebuggingServer localhost:1025



## install

pip install django

pip install python-dateutil

pip install django-anymail[mailgun]

pip install django-crontab

pip install psycopg2

#### how to use crontab

python manage.py crontab add

python manage.py crontab show

python manage.py crontab remove



## i18n

python manage.py makemessages -l zh_Hans 

!!!在setting里面是zh-hans 语言包是下划线 不然有空格的英文将无法被翻译

!!!在debian上语言包名字为 zh_Hans 大写H 不然也会出奇怪问题 

python manage.py makemessages -a

python manage.py compilemessages



## todo

- [ ] Save traffic to redis and show it in graphic 
- [x] useful front page
- [ ] add alipay
- [x] restructure v2ray sidecar
- [x] add support to ss
- [ ] add support to trojan
- [x] make dashboard support mobile
- [x] make interface simple , no need to support mobile
- [x] recode invite code
