from django.db import models


# from django.contrib.auth.models import AbstractUser

# Create your models here.
# 总账户
class Total_brank_account(models.Model):
    datess = models.DateTimeField(verbose_name='创建日期', )
    total_account_name = models.CharField(verbose_name='总账户名', max_length=64)
    total_brank_name = models.CharField(verbose_name='银行名', max_length=64)
    total_brank_number = models.CharField(verbose_name='开户行号', max_length=32)
    total_brank_card_number = models.CharField(verbose_name='银行卡号', max_length=32)
    deletes = models.CharField(max_length=5)

    # def __str__(self):
    #     return self.total_account_name


# 店铺表
class Shops(models.Model):
    shopname = models.CharField(verbose_name='店铺名', max_length=64)
    own_total_brank = models.ForeignKey(Total_brank_account, on_delete=models.CASCADE)
    deletes = models.CharField(max_length=5)

    def __str__(self):
        return self.shopname


# 用户表
class Userinfo(models.Model):
    passwd = models.CharField(verbose_name='密码', max_length=16)
    username = models.CharField(verbose_name='用户名', max_length=32, )
    rouse = models.CharField(verbose_name='角色', max_length=8)
    description = models.CharField(u'职位描述', max_length=64)
    shop = models.ManyToManyField("Shops")
    total_brank_account = models.ManyToManyField("Total_brank_account")
    deletes = models.CharField(max_length=5)


# 子账户
class Brank_account(models.Model):
    account_name = models.CharField(verbose_name='账户名', max_length=64)
    brank_name = models.CharField(verbose_name='银行名', max_length=64)
    brank_number = models.CharField(verbose_name='开户行号', max_length=32)
    brank_card_number = models.CharField(verbose_name='银行卡号', max_length=32)
    brank_operator = models.ManyToManyField("Userinfo")
    total_account_name = models.ForeignKey(Total_brank_account, on_delete=models.CASCADE)
    deletes = models.CharField(max_length=5)


# 子账户记录
class Account_record(models.Model):
    datess = models.DateTimeField(verbose_name='创建日期',)
    account_name = models.ForeignKey(Brank_account, on_delete=models.CASCADE)
    start_money = models.IntegerField(verbose_name='初始资金')
    end_money = models.IntegerField(verbose_name='结余资金')
    weixin_withdraw_money = models.IntegerField(verbose_name='微信提现手续费')
    operator = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    makes = models.CharField(max_length=5, verbose_name='运营确认')
    start_money_img = models.ImageField(upload_to='start_img')
    end_money_img = models.ImageField(upload_to='end_img')
    weixin_img = models.ImageField(upload_to='weixin_img')
    deletes = models.CharField(max_length=5)


# 总账户记录
class Total_account_record(models.Model):
    datess = models.DateTimeField(verbose_name='创建日期', )
    account_name = models.ForeignKey(Total_brank_account, on_delete=models.CASCADE)
    start_money = models.IntegerField(verbose_name='初始资金')
    end_money = models.IntegerField(verbose_name='结余资金')
    operator = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    makes = models.CharField(max_length=5, verbose_name='运营确认')
    start_money_img = models.ImageField(upload_to='start_img')
    end_money_img = models.ImageField(upload_to='end_img')
    deletes = models.CharField(max_length=5)


# 喝酒记录
class Brush_single_entry(models.Model):
    shopname = models.CharField(verbose_name='店铺名', max_length=32)
    qq_or_weixin = models.CharField(verbose_name='QQ或微信', max_length=32)
    wang_wang_number = models.CharField(verbose_name='旺旺号', max_length=32)
    online_order_number = models.CharField(verbose_name='线上订单号', max_length=26)
    transaction_data = models.CharField(verbose_name='成交日期', max_length=16)
    payment_type = models.CharField(verbose_name='付款类型', max_length=16)
    payment_amount = models.CharField(verbose_name='付款金额', max_length=10)
    payment_account = models.ForeignKey(Brank_account, on_delete=models.CASCADE)
    operator = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    remarks = models.CharField(verbose_name='备注', max_length=64)
    add_time = models.DateTimeField(verbose_name='创建日期', auto_now=True, )
    deletes = models.CharField(max_length=5)


# 日志
class Log(models.Model):
    add_time = models.DateTimeField(verbose_name='操作日期', auto_now=True, )
    operator = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    operation_type = models.CharField(verbose_name='操作类型', max_length=32)
    before_operation = models.CharField(verbose_name='操作前', max_length=600)
    after_operation = models.CharField(verbose_name='操作后', max_length=600)
