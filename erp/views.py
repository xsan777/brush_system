from django.shortcuts import render, HttpResponse
from brush.models import *
from erp.models import *
import json


# Create your views here.


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

#通过旺旺号查询
def search_by_wangwang_num(request):
    asd = '219441250672567971'
    wang_wang_numbers = request.GET.get('wangwang_num')
    # order_num = Brush_single_entry.objects.using('default').get(wang_wang_number=wang_wang_numbers, deletes=False)
    search_o_id = JstOrdersQuery.objects.using('erp_database').filter(shop_buyer_id=wang_wang_numbers).last()
    search_o_id = JstOrdersQuerySpecialSingle.objects.using('erp_database').get(o_id=search_o_id.o_id)
    msg = {'pay_date':str(search_o_id.pay_date),'shop_name':search_o_id.shop_name,}
    msg = json.dumps(msg)
    return HttpResponse(msg)
