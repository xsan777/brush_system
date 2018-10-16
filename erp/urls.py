from django.urls import path
from erp import views
urlpatterns = [
    path('search_by_order_num/',views.search_by_order_num),
    path('search_by_wangwang_num/',views.search_by_wangwang_num),
    path('search_by_wangwang_num2/',views.search_by_wangwang_num2),
    path('search_by_online_order_number/',views.search_by_online_order_number),
]