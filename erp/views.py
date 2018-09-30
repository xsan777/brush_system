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


# 通过订单号查询
def search_by_order_num(request):
    asd = '219441250672567971'
    online_order_numbers = request.GET.get('oreder_num')
    print(online_order_numbers)
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
