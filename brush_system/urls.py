"""Brush_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from brush import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login),
    path('update_passwd/',views.update_passwd),
    path('erp/',include('erp.urls')),
    path('total_brankmanagement/',views.total_brank_management),
    path('verification_total_account/',views.verification_total_account),
    path('shopmanagement/', views.shopmanagement),
    path('verification_shopname/',views.verification_shopname),
    path('edit_shop/',views.edit_shop),
    path('usermanagement/', views.adduser),
    path('adduser/', views.adduser),
    path('verification_username/',views.verification_username),
    path('brankmanagement/', views.brankmanagement),
    path('verification_brank/',views.verification_brank),
    path('countmanagement/', views.countmanagement),
    path('total_countmanagement/', views.total_countmanagement),
    path('brushmanagement/', views.brushmanagement),
    path('brushmanagement2/', views.brushmanagement_2),
    path('edit/',views.edit),
    path('edit_total_brank/',views.edit_total_brank),
    path('edit_user/',views.edit_user),
    path('edit_count/',views.edit_count),
    path('edit_count_2/',views.edit_count_2),
    path('edit_total_count/',views.edit_total_count),
    path('edit_brank/',views.edit_brank),
    path('deletes/',views.delete_data),
    path('del_total_brank/',views.del_total_brank),
    path('deletes_user/',views.deletes_user),
    path('deletes_shop/',views.delete_shop),
    path('deletes_count/',views.deletes_count),
    path('delete_total_count/',views.delete_total_count),
    path('deletes_brank/',views.deletes_brank),
    path('more_date/',views.more_date),
    path('chose_operator/',views.chose_operator),
    path('check_account/',views.check_account),
    path('check_total_account/',views.check_total_account),
    path('make_account/',views.make_account),
    path('make_total_account/',views.make_total_account),
    path('search_count/',views.search_count),
    path('search_total_count/',views.search_total_count),
    path('search_online_order_num_brush_data/',views.search_online_order_num_brush_data),
    path('shop_bill/',views.shop_bill),
    path('account_bill/',views.account_bill),
    path('total_account_bill/',views.total_account_bill),
    path('all_data/',views.all_data),
    path('download_brush/',views.download_brush),
    path('down_shop_bill/',views.down_shop_bill),
    path('down_shop_bill2/',views.down_shop_bill2),
    path('down_total_account_brush/',views.down_total_account_brush),
    path('down_total_account_brush2/',views.down_total_account_brush2),
    path('down_all_data/',views.down_all_data),
    path('down_all_data2/',views.down_all_data2),
    path('Upload_excel/',views.upload_excel),
    path('upload_data/',views.upload_data),
    path('template_file_download/',views.template_file_download),
    path('supplemental_upload_excel/',views.supplemental_upload_excel),
    path('supplemental_upload_data/',views.supplemental_upload_data),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
