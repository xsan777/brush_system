from django.shortcuts import render, HttpResponse
from brush.models import *
from erp.models import *
import json, datetime, time


# Create your views here.
# 获取前n天的日期
def get_nday_list2(n, now_time):
    dd = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    before_n_days2 = []
    for i in range(1, n + 1)[::-1]:
        bb = str(dd - datetime.timedelta(days=i - 1))
        aa = bb.replace(' 00:00:00', '')
        before_n_days2.append(aa)
    return before_n_days2[0]


# 喝酒数据与erp数据相互验证
# 状态正确返回0，不正确返回其他的数字
class Verification(object):
    # 验证线上订单号是否存在
    def order_online(self, order_online_num, ):
        order_stats = JstOrdersQuery.objects.using('erp_database').filter(so_id=order_online_num).all()
        if len(order_stats) > 0:
            for i in order_stats:
                search_o_id = i.o_id
            return 0, search_o_id
        else:
            special_order_stats = ''
            return 1, special_order_stats

    # 验证该线上订单号是否为特殊单
    def special_order(self, search_o_id):
        special_order_stats = JstOrdersQuerySpecialSingle.objects.using('erp_database').filter(o_id=search_o_id).all()
        if len(special_order_stats) > 0:
            return 0
        else:
            return 2

    # 因特殊单数据库新增了线上订单号和旺旺号字段，所以重写了验证该线上订单号是否为特殊单函数，由于之前的数据仍然没有这两个字段的内容，所以先执行这个函数，如果没有查到则执行原先的先从erp总表查o_id再通过o_id去特殊单表里查询
    def special_order_2(self, online_order_number):
        special_order_stats = JstOrdersQuerySpecialSingle.objects.using('erp_database').filter().all()
        if len(special_order_stats) > 0:
            return 0
        else:
            return 2


# 查询线上订单号的状态：online_order_number_exit = 0 代表该线上订单号不存在；online_order_number_exit = 1代表可能为实包
def search_by_online_order_number(request):
    online_order_number = request.POST.get('online_order_number')
    verification = Verification()
    online_order_number_exit, search_o_id = verification.order_online(online_order_number)[0], verification.order_online(online_order_number)[1]
    if online_order_number_exit == 0:
        online_order_number_exit = verification.special_order(online_order_number, search_o_id)
    msg = json.dumps(online_order_number_exit)
    return HttpResponse(msg)


# 通过订单号查询
def search_by_order_num(request):
    asd = '219441250672567971'
    online_order_numbers = request.GET.get('oreder_num')
    order_num = Brush_single_entry.objects.using('default').get(online_order_number=online_order_numbers, deletes=False)
    search_o_id = JstOrdersQuery.objects.using('erp_database').get(so_id=order_num.online_order_number)
    print(search_o_id.pay_date)
    msg = json.dumps(str(search_o_id.pay_date))
    return HttpResponse(msg)


# 通过旺旺号查询近90天的喝酒数据
def search_by_wangwang_num(request):
    wang_wang_numbers = request.GET.get('wangwang_num')
    wang_wang_numbers = str(wang_wang_numbers).strip()
    # order_num = Brush_single_entry.objects.using('default').get(wang_wang_number=wang_wang_numbers, deletes=False)
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    search_o_id = JstOrdersQuery.objects.using('erp_database').filter(pay_date__gte=get_nday_list2(90, now_time),
                                                                      shop_buyer_id=wang_wang_numbers).all()
    msg = ''
    for i in search_o_id:
        search_o_id2 = JstOrdersQuerySpecialSingle.objects.using('erp_database').get(o_id=i.o_id)
        msg = msg + '喝酒时间：' + str(i.pay_date) + '<br/> ' + '喝酒店铺：' + search_o_id2.shop_name + '<br/>'
    if msg == '':
        msg = '该旺旺号之前没有喝酒'
    msg = json.dumps(msg)
    return HttpResponse(msg)


# 通过旺旺号查询最近一次喝酒数据
def search_by_wangwang_num2(request):
    wang_wang_numbers = request.GET.get('wangwang_num')
    wang_wang_numbers = str(wang_wang_numbers).strip()
    # order_num = Brush_single_entry.objects.using('default').get(wang_wang_number=wang_wang_numbers, deletes=False)
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    search_o_id = JstOrdersQuery.objects.using('erp_database').filter(pay_date__gte=get_nday_list2(90, now_time),
                                                                      shop_buyer_id=wang_wang_numbers).last()
    search_o_id2 = JstOrdersQuerySpecialSingle.objects.using('erp_database').get(o_id=search_o_id.o_id)
    msg = '上次喝酒时间：' + str(search_o_id.pay_date) + '<br/> ' + '喝酒店铺：' + search_o_id2.shop_name + '<br/>'
    msg = json.dumps(msg)
    return HttpResponse(msg)
