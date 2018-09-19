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
    path('admin/', admin.site.urls),
    path('', views.login),
    path('erp/',include('erp.urls')),
    path('log_out/', views.log_out),
    path('shopmanagement/', views.shopmanagement),
    path('verification_shopname/',views.verification_shopname),
    path('edit_shop/',views.edit_shop),
    path('usermanagement/', views.adduser),
    path('adduser/', views.adduser),
    path('verification_username/',views.verification_username),
    path('brankmanagement/', views.brankmanagement),
    path('verification_brank/',views.verification_brank),
    path('countmanagement/', views.countmanagement),
    path('brushmanagement/', views.brushmanagement),
    path('edit/',views.edit),
    path('edit_user/',views.edit_user),
    path('edit_count/',views.edit_count),
    path('edit_brank/',views.edit_brank),
    path('deletes/',views.delete_data),
    path('deletes_user/',views.deletes_user),
    path('deletes_shop/',views.delete_shop),
    path('deletes_count/',views.deletes_count),
    path('deletes_brank/',views.deletes_brank),
    path('more_date/',views.more_date),
    path('chose_shop/',views.chose_shop),
    path('check_account/',views.check_account),
    path('make_account/',views.make_account),
    path('search_count/',views.search_count),
    path('shop_bill/',views.shop_bill),
    path('account_bill/',views.account_bill),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
