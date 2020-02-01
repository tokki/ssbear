# Generated by Django 2.2.9 on 2020-02-01 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='content_cn',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='title_cn',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='info_cn',
        ),
        migrations.RemoveField(
            model_name='node',
            name='description_cn',
        ),
        migrations.RemoveField(
            model_name='node',
            name='name_cn',
        ),
        migrations.RemoveField(
            model_name='service',
            name='description_cn',
        ),
        migrations.RemoveField(
            model_name='service',
            name='title_cn',
        ),
        migrations.AlterField(
            model_name='bill',
            name='payment',
            field=models.IntegerField(choices=[(0, 'alipay当面付'), (1, '邀请用户奖励'), (5, '购买服务')], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '运行中')], default=0),
        ),
        migrations.AlterField(
            model_name='trafficlog',
            name='traffic_down',
            field=models.BigIntegerField(default=0, verbose_name='下载数据量'),
        ),
        migrations.AlterField(
            model_name='trafficlog',
            name='traffic_up',
            field=models.BigIntegerField(default=0, verbose_name='上传数据量'),
        ),
    ]