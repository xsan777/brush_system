from django.db import models


# from django.contrib.auth.models import AbstractUser

# Create your models here.
class Shops(models.Model):
    shopname = models.CharField(verbose_name='店铺名', max_length=64)
    deletes = models.CharField(max_length=5)

    def __str__(self):
        return self.shopname


class Userinfo(models.Model):
    passwd = models.CharField(verbose_name='密码', max_length=16)
    username = models.CharField(verbose_name='用户名', max_length=32,)
    rouse = models.CharField(verbose_name='角色', max_length=8)
    description = models.CharField(u'职位描述', max_length=64)
    shop = models.ManyToManyField("Shops")
    deletes = models.CharField(max_length=5)


class Brank_account(models.Model):
    account_name = models.CharField(verbose_name='账户名', max_length=64)
    brank_name = models.CharField(verbose_name='银行名', max_length=64)
    brank_number = models.CharField(verbose_name='开户行号', max_length=32)
    brank_card_number = models.CharField(verbose_name='银行卡号', max_length=32)
    brank_operator = models.ManyToManyField("Userinfo")
    deletes = models.CharField(max_length=5)


class Account_record(models.Model):
    datess = models.DateTimeField(verbose_name='创建日期',)
    # account_name = models.CharField(verbose_name='账户名', max_length=32)
    account_name = models.ForeignKey(Brank_account,on_delete=models.DO_NOTHING)
    start_money = models.IntegerField(verbose_name='初始资金')
    end_money = models.IntegerField(verbose_name='结余资金')
    # operator = models.CharField(verbose_name='操作员', max_length=16)
    operator = models.ForeignKey(Userinfo,on_delete=models.DO_NOTHING)
    makes = models.CharField(max_length=5, verbose_name='运营确认')
    start_money_img = models.ImageField(upload_to='img')
    end_money_img = models.ImageField(upload_to='img')
    deletes = models.CharField(max_length=5)


class Brush_single_entry(models.Model):
    shopname = models.CharField(verbose_name='店铺名', max_length=32)
    qq_or_weixin = models.CharField(verbose_name='QQ或微信', max_length=32)
    wang_wang_number = models.CharField(verbose_name='旺旺号', max_length=32)
    online_order_number = models.CharField(verbose_name='线上订单号', max_length=26)
    transaction_data = models.CharField(verbose_name='成交日期', max_length=16)
    payment_type = models.CharField(verbose_name='付款类型', max_length=16)
    payment_amount = models.CharField(verbose_name='付款金额', max_length=10)
    # payment_account = models.CharField(verbose_name='付款账户', max_length=32)
    payment_account = models.ForeignKey(Brank_account,on_delete=models.DO_NOTHING)
    # operator = models.CharField(verbose_name='操作员', max_length=16)
    operator = models.ForeignKey(Userinfo,on_delete=models.DO_NOTHING)
    remarks = models.CharField(verbose_name='备注', max_length=64)
    add_time = models.DateTimeField(verbose_name='创建日期', auto_now=True,)
    deletes = models.CharField(max_length=5)


class Log(models.Model):
    add_time = models.DateTimeField(verbose_name='操作日期', auto_now=True, )
    # operator = models.CharField(verbose_name='操作员', max_length=16)
    operator = models.ForeignKey(Userinfo,on_delete=models.DO_NOTHING)
    operation_type = models.CharField(verbose_name='操作类型', max_length=32)
    before_operation = models.CharField(verbose_name='操作前', max_length=500)
    after_operation = models.CharField(verbose_name='操作后', max_length=500)
