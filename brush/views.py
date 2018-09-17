from django.shortcuts import render, HttpResponse, redirect
from brush.models import *
import time, json, datetime
from .forms import *


# Create your views here.
# 将时间2018-08-29 16:18:53.986855转换成2018年08月29日 16:18
def t(times):
    times = str(times)
    time1 = times.split(' ')
    time2 = time1[0].split('-')
    year1 = time2[0]
    if time2[1][0] == '0':
        mouth1 = time2[1][1]
    else:
        mouth1 = time2[1]
    day1 = time2[2]
    if len(day1) > 1:
        day1 = str(day1)[1]
    times = '%s年%s月%s日 ' % (year1, mouth1, day1)
    time3 = time1[1].split(':')
    hours = time3[0]
    minits = time3[1]
    timess = '%s:%s' % (hours, minits)
    end_time = times + timess
    return end_time


# 获取前2天的日期
def get_nday_list2(n, now_time):
    dd = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    before_n_days2 = []
    for i in range(1, n + 1)[::-1]:
        bb = str(dd - datetime.timedelta(days=i - 1))
        aa = bb.replace(' 00:00:00', '')
        before_n_days2.append(aa)
    return before_n_days2[0]


# 登录
def login(request):
    msg = ''
    if request.method == 'POST':
        usernam = request.POST.get('user')
        passwd = request.POST.get('passwd')
        user = Userinfo.objects.filter(username=usernam, deletes=False)
        if user:
            user = Userinfo.objects.filter(username=usernam, deletes=False).values('passwd', 'rouse', ).get()
            if passwd == user['passwd']:
                request.session['username'] = usernam
                request.session['rouse'] = user['rouse']
                request.session.set_expiry(0)
                if user['rouse'] == '运营':
                    return redirect('brushmanagement/')
                else:
                    return redirect(to=countmanagement)
        msg = '用户名或密码错误'
    return render(request, 'login.html', {'err_msg': msg})


# 退出
def log_out(request):
    user = request.session.get('username')
    return redirect(to=login)


# 用户管理
def adduser(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '用户管理'
    err_msg = ''
    msgs = ''
    users = request.GET.get('username')
    if users:
        user_id = Userinfo.objects.filter(username=users, deletes=False).all()
    else:
        user_id = Userinfo.objects.filter(deletes=False).all()
    if request.method == 'POST':
        usernames = request.POST.get('username')
        passwds = request.POST.get('passwd')
        passwd2s = request.POST.get('passwd2')
        rouses = request.POST.get('rose')
        descriptions = request.POST.get('description')
        shop_list = request.POST.getlist('checkitem')
        if rouses == '财务':
            shop_all = Shops.objects.filter(deletes=False).all()
            shop_list = []
            for j in shop_all:
                shop_list.append(j.shopname)
        if passwd2s == passwds:
            if len(shop_list) != 0:
                Userinfo.objects.create(username=usernames, passwd=passwds, rouse=rouses, description=descriptions, deletes=False)
                user_ids = Userinfo.objects.filter(username=usernames, deletes=False).get()
                # 将店铺与用户绑定
                for shop in shop_list:
                    user_ids.shop.add(Shops.objects.get(shopname=shop))
                last_date = Userinfo.objects.last()
                shops_clean = last_date.shop.all()
                shops = ''
                for user_shop in shops_clean:
                    shops += str(user_shop)
                    shops += '、'
                operators = Userinfo.objects.get(username=user, deletes=False)
                operation_types = '创建新用户'
                after_operations = '{id：%d，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s}' % (last_date.id, usernames, passwds, rouse, descriptions, shops)
                Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
            else:
                msgs = '必须选择店铺'
        else:
            err_msg = '两次密码输入不一致'
    table_list = []
    for i in user_id:
        tables = {}
        tables['id'] = i.id
        tables['username'] = i.username
        tables['rouse'] = i.rouse
        tables['description'] = i.description
        shops = ''
        if i.rouse == '财务':
            shops = '所有店铺'
        else:
            for user_shop in i.shop.filter(deletes=False).all():
                shops += str(user_shop)
                shops += '、'
        tables['shop'] = shops
        table_list.append(tables)
    shopss = Shops.objects.filter(deletes=False).all()
    add_form = Add_user()
    edit_form = Edit_user()

    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'user.html',
                  {'title': title, 'tables': table_list, 'shops': shopss, 'add_form': add_form, 'edit_user': edit_form, 'err_msg': err_msg,
                   'msgs': msgs, 'user': user, 'admin_flog': admin_flog})


# 用户名验证
def verification_username(request):
    usernames = request.GET.get('username')
    user_exist = Userinfo.objects.filter(username=usernames, deletes=False).all()
    if user_exist:
        msg = json.dumps('用户名已存在')
    else:
        msg = json.dumps('')
    return HttpResponse(msg)


# 搜索用户信息
def search_ueser(request):
    title = '用户管理'
    users = request.GET.get('username')
    tables = Userinfo.objects.filter(username=users, deletes=False).all()
    shopss = Shops.objects.filter(deletes=False).all()
    add_form = Add_user()
    edit_form = Edit_user()
    return render(request, 'user.html', {'title': title, 'tables': tables, 'shops': shopss, 'add_form': add_form, 'edit_user': edit_form, })


# 编辑用户信息
def edit_user(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    err_msg = ''
    if request.method == 'POST':
        ids = request.POST.get('id')

        passwds = request.POST.get('passwd')
        passwd2s = request.POST.get('passwd2')
        rouses = request.POST.get('rose')
        descriptions = request.POST.get('description')
        shop_list = request.POST.getlist('checkitem')
        if rouses == '财务':
            shop_all = Shops.objects.filter(deletes=False).all()
            shop_list = []
            for j in shop_all:
                shop_list.append(j.shopname)
        if passwd2s == passwds:
            if len(shop_list) != 0:
                user_id = Userinfo.objects.get(id=ids)
                usernames = user_id.username
                Userinfo.objects.filter(id=ids).update(username=usernames, passwd=passwds, rouse=rouses, description=descriptions, deletes=False)
                user_id.shop.clear()
                # 将店铺与用户绑定
                for shop in shop_list:
                    user_id.shop.add(Shops.objects.get(shopname=shop))
                shops_clean = user_id.shop.all()
                shops = ''
                for user_shop in shops_clean:
                    shops += str(user_shop)
                    shops += '、'
                update_date = Userinfo.objects.get(id=ids)
                shops_clean = update_date.shop.all()
                shops = ''
                for user_shop in shops_clean:
                    shops += str(user_shop)
                    shops += '、'
                operators = Userinfo.objects.get(username=user, deletes=False)
                operation_types = '修改用户信息'
                before_operations = '{id：%d，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s}' % (
                    user_id.id, user_id.username, user_id.passwd, user_id.rouse, user_id.description, shops)
                after_operations = '{id：%s，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s}' % (ids, usernames, passwds, rouse, descriptions, shops)
                Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                                   before_operation=before_operations)
            else:
                err_msg = '必须选择店铺'
    current_data = Userinfo.objects.filter(id=ids).get()
    msg = json.dumps(
        {'rose': current_data.rouse, 'username': current_data.username, 'passwd': current_data.passwd, 'description': current_data.description,
         'ids': current_data.id, 'err': err_msg})
    return HttpResponse(msg)


# 删除用户
def deletes_user(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    Userinfo.objects.filter(id=ids).update(deletes='True')
    last_data = Userinfo.objects.get(id=ids)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除用户'
    after_operations = '删除了{id：%s，用户名：%s}' % (ids, last_data.username)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
    return HttpResponse('ok')


# 店铺管理
def shopmanagement(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '店铺管理'
    shop_name = request.GET.get('shop_name')
    if shop_name:
        shop_all = Shops.objects.filter(shopname=shop_name, deletes=False).all()
    else:
        shop_all = Shops.objects.filter(deletes=False).all()
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        Shops.objects.create(shopname=shop_name, deletes=False)
        # 财务账号自动绑定新开店铺
        user_need = Userinfo.objects.filter(rouse='财务', deletes=False).all()
        for user_add in user_need:
            user_add.shop.add(Shops.objects.get(shopname=shop_name, deletes=False))

        last_date = Shops.objects.last()
        operation_types = '添加店铺'
        after_operations = '{id：%d，店铺名：%s}' % (last_date.id, shop_name)
        Log.objects.create(operator=Userinfo.objects.get(username=user, deletes=False), operation_type=operation_types,
                           after_operation=after_operations)
    shop_info = []
    for shop in shop_all:
        tables = {}
        tables['shop_name'] = shop.shopname
        tables['id'] = shop.id
        owners = ''
        for owner in shop.userinfo_set.filter(deletes=False).all():
            owners += str(owner.username)
            owners += '、'
        tables['shop_owners'] = owners
        shop_info.append(tables)
    add_shop_form = Add_shop_form()
    edit_shop_form = Edit_shop_form()
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'shops.html',
                  {'title': title, 'tables': shop_info, 'add_shop_form': add_shop_form, 'edit_shop_form': edit_shop_form, 'user': user,
                   'admin_flog': admin_flog})


# 查找店铺
def seach_shop(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '店铺管理'
    shop_name = request.GET.get('shop_name')
    tables = Shops.objects.filter(shopname=shop_name, deletes=False).all()
    shop_info = []
    for shop in tables:
        tables = {}
        tables['shop_name'] = shop.shopname
        tables['id'] = shop.id
        owners = ''
        for owner in shop.userinfo_set.all():
            owners += str(owner.username)
            owners += '、'
        tables['shop_owners'] = owners
        shop_info.append(tables)
    add_shop_form = Add_shop_form()
    edit_shop_form = Edit_shop_form()
    return render(request, 'shops.html',
                  {'title': title, 'tables': shop_info, 'add_shop_form': add_shop_form, 'edit_shop_form': edit_shop_form, 'user': user})


# 店铺名验证
def verification_shopname(request):
    shopnames = request.GET.get('shopname')
    user_exist = Shops.objects.filter(shopname=shopnames, deletes=False).all()
    if user_exist:
        msg = json.dumps('店铺名已存在')
    else:
        msg = json.dumps('')
    return HttpResponse(msg)


# 修改店铺名
def edit_shop(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    if request.method == 'POST':
        ids = request.POST.get('id')
        shop_names = request.POST.get('shop_name')
        before_shopname = Shops.objects.filter(id=ids).values('shopname').get()
        Shops.objects.filter(id=ids).update(shopname=shop_names, deletes=False)
        operators = Userinfo.objects.get(username=user, deletes=False)
        operation_types = '修改店铺名'
        before_operations = '{id：%s，店铺名：%s}' % (ids, before_shopname['shopname'])
        after_operations = '{id：%s，店铺名：%s}' % (ids, shop_names)
        Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations, after_operation=after_operations)
        return redirect(to=shopmanagement)
    before_shopname = Shops.objects.filter(id=ids).values('shopname').get()
    msg = json.dumps({'ids': ids, 'shopname': before_shopname['shopname']})
    return HttpResponse(msg)


# 删除店铺
def delete_shop(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    delete_shops = Shops.objects.filter(id=ids).values('shopname').get()
    delete_shop_name = delete_shops['shopname']
    Shops.objects.filter(id=ids).update(deletes=True)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除店铺'
    after_operations = '删除了{id：%s，店铺名：%s}' % (ids, delete_shop_name)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
    return redirect(to=shopmanagement)


# 银行账户管理
def brankmanagement(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '银行账户管理'
    account_names = request.GET.get('account_name')
    if account_names:
        tables = Brank_account.objects.filter(account_name=account_names, deletes=False).all()
    else:
        tables = Brank_account.objects.filter(deletes=False).all()
    user_list = Userinfo.objects.filter(deletes=False).all()
    add_brank_account_form = Add_brank_account()
    edit_brank_account_form = Edit_brank_account()
    msg = ''
    if request.method == 'POST':
        account_names = request.POST.get('account_name')
        brank_names = request.POST.get('brank_name')
        brank_numbers = request.POST.get('brank_number')
        brank_card_numbers = request.POST.get('brank_card_number')
        brank_operator_list = request.POST.getlist('checkitem')
        if len(brank_operator_list) != 0:
            Brank_account.objects.create(account_name=account_names, brank_name=brank_names, brank_number=brank_numbers,
                                         brank_card_number=brank_card_numbers, deletes=False)
            brank_card_id = Brank_account.objects.filter(account_name=account_names, deletes=False).get()
            for users in brank_operator_list:
                brank_card_id.brank_operator.add(Userinfo.objects.get(username=users, deletes=False))
            user_clean = brank_card_id.brank_operator.all()
            brank_operator_lists = ''
            for user_brank in user_clean:
                brank_operator_lists += str(user_brank.username)
                brank_operator_lists += '、'
            operation_types = '创建银行账户'
            after_operations = '{id：%d，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，银行卡操作人：%s}' % (
                brank_card_id.id, account_names, brank_names, brank_numbers, brank_card_numbers, brank_operator_lists)
            Log.objects.create(operator=Userinfo.objects.get(username=user, deletes=False), operation_type=operation_types,
                               after_operation=after_operations)
        else:
            msg = '必须选择银行卡使用人'
    table_list = []
    for i in tables:
        tables = {}
        tables['id'] = i.id
        tables['account_name'] = i.account_name
        tables['brank_name'] = i.brank_name
        tables['brank_card_number'] = i.brank_card_number
        tables['brank_number'] = i.brank_number
        brankers = ''
        for user_brank in i.brank_operator.filter(deletes=False).all():
            brankers += str(user_brank.username)
            brankers += '、'
        tables['brank_owner'] = brankers
        table_list.append(tables)
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'brankmanagement.html',
                  {'title': title, 'tables': table_list, 'add_brank_account_form': add_brank_account_form, 'user_list': user_list, 'msg': msg,
                   'edit_brank_account_form': edit_brank_account_form, 'user': user, 'admin_flog': admin_flog})


# 搜索银行账户
def search_brank(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '银行账户管理'
    account_names = request.GET.get('account_name')
    tables = Brank_account.objects.filter(account_name=account_names, deletes=False).all()
    table_list = []
    for i in tables:
        tables = {}
        tables['id'] = i.id
        tables['account_name'] = i.account_name
        tables['brank_name'] = i.brank_name
        tables['brank_card_number'] = i.brank_card_number
        tables['brank_number'] = i.brank_number
        brankers = ''
        for user_brank in i.brank_operator.filter(deletes=False).all():
            brankers += str(user_brank.username)
            brankers += '、'
        tables['brank_owner'] = brankers
        table_list.append(tables)
    add_brank_account_form = Add_brank_account()
    edit_brank_account_form = Edit_brank_account()
    return render(request, 'brankmanagement.html',
                  {'title': title, 'tables': table_list, 'add_brank_account_form': add_brank_account_form,
                   'edit_brank_account_form': edit_brank_account_form, 'user': user})


# 验证银行账户
def verification_brank(request):
    account_names = request.GET.get('account_name')
    brank_card_numbers = request.GET.get('brank_card_number')
    verification = Brank_account.objects.filter(account_name=account_names, deletes=False)
    verification2 = Brank_account.objects.filter(brank_card_number=brank_card_numbers, deletes=False)
    if verification:
        msg = json.dumps('该账户已存在')
        return HttpResponse(msg)
    if verification2:
        msg = json.dumps('该卡号已存在')
    else:
        msg = json.dumps('')
    return HttpResponse(msg)


# 修改银行账户信息
def edit_brank(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    msgss = ''
    if request.method == 'POST':
        ids = request.POST.get('id')
        account_names = request.POST.get('account_name')
        brank_names = request.POST.get('brank_name')
        brank_numbers = request.POST.get('brank_number')
        brank_card_numbers = request.POST.get('brank_card_number')
        brank_operator_list = request.POST.getlist('checkitem')
        if len(brank_operator_list) != 0:
            brank_card_id = Brank_account.objects.get(id=ids)
            Brank_account.objects.filter(id=ids).update(account_name=account_names, brank_name=brank_names, brank_number=brank_numbers,
                                                        brank_card_number=brank_card_numbers, deletes=False)
            brank_card_id2 = Brank_account.objects.filter(account_name=account_names, deletes=False).get()
            brank_card_id2.brank_operator.clear()
            for users in brank_operator_list:
                brank_card_id2.brank_operator.add(Userinfo.objects.get(username=users, deletes=False))
            user_clean = brank_card_id2.brank_operator.all()
            before_operation_lists = ''
            for before_operations in brank_card_id.brank_operator.all():
                before_operation_lists += str(before_operations.username)
                before_operation_lists += '、'
            brank_operator_lists = ''
            for user_brank in user_clean:
                brank_operator_lists += str(user_brank.username)
                brank_operator_lists += '、'
            operation_types = '修改银行账户'
            operators = Userinfo.objects.get(username=user, deletes=False)
            before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，银行卡操作人：%s}' % (
                ids, brank_card_id.account_name, brank_card_id.brank_name, brank_card_id.brank_number, brank_card_id.brank_card_number,
                before_operation_lists)
            after_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，银行卡操作人：%s}' % (
                ids, account_names, brank_names, brank_numbers, brank_card_numbers, brank_operator_lists)
            Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                               before_operation=before_operations)
        else:
            msgss = '必须选择银行卡使用人'

    current_data = Brank_account.objects.filter(id=ids, deletes=False).get()
    msg = json.dumps({'account_name': current_data.account_name, 'brank_name': current_data.brank_name, 'brank_number': current_data.brank_number,
                      'brank_card_number': current_data.brank_card_number, 'ids': current_data.id, 'err': msgss, 'ids': ids})
    return HttpResponse(msg)


# 删除银行账户
def deletes_brank(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    Brank_account.objects.filter(id=ids).update(deletes='True')
    brank_card_id = Brank_account.objects.filter(id=ids).get()
    before_operation_lists = ''
    for before_operations in brank_card_id.brank_operator.all():
        before_operation_lists += str(before_operations.username)
        before_operation_lists += '、'
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除银行账户'
    before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，银行卡操作人：%s}' % (
        ids, brank_card_id.account_name, brank_card_id.brank_name, brank_card_id.brank_number, brank_card_id.brank_card_number,
        before_operation_lists)
    after_operations = '删除了id=%s的银行账户' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return HttpResponse('ok')


# 账户记录管理
def countmanagement(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '账户记录管理'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    add_times = datetime.datetime.now()
    account = Brank_account.objects.filter(brank_operator__username=user, deletes=False).all()
    if rouse == '财务':
        count = Account_record.objects.filter(datess__date=now_time, deletes=False).all()
    else:
        count = Account_record.objects.filter(datess__date=now_time, operator__username=user, deletes=False).all()
    forms = Forms()
    edit_form = Edit_forms()
    errs = ''
    if request.method == 'POST':
        account_names = request.POST.get('account_name')
        print(account_names)
        if account_names  == None:
            errs = '账户名不能为空'
        else:
            exits = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=account_names, deletes=False).all()
            if len(exits) == 0:
                operators = Userinfo.objects.get(username=user, deletes=False)
                form_data = Forms(request.POST)
                if form_data.is_valid():
                    data = form_data.clean()
                    start_moneys = data['start_money']
                    end_moneys = data['end_money']
                    try:
                        float(start_moneys)
                        float(end_moneys)
                        errs = ''
                    except ValueError:
                        errs = '初始资金和结余资金必须为数字'
                    if errs == '':
                        account_names = Brank_account.objects.get(account_name=account_names, deletes=False)
                        Account_record.objects.create(datess=add_times, account_name=account_names, start_money=start_moneys, end_money=end_moneys,
                                                      operator=operators, makes='False', start_money_img=request.FILES.get('start_money_img'),
                                                      end_money_img=request.FILES.get('end_money_img'), deletes=False)
                        last_date = Account_record.objects.last()

                        operation_types = '创建账户记录'
                        after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s}' % (
                            last_date.id, account_names.account_name, start_moneys, end_moneys, user, last_date.start_money_img, last_date.end_money_img)
                        Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
            else:
                errs = '该账户今日已创建记录'
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    for i in account:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    if rouse == '运营':
        return render(request, 'countmanagement2.html',
                      {'title': title, 'account': account, 'count': count, 'nowss': now_time, 'formm': forms, 'edit_form': edit_form, 'errs': errs,
                       'user': user, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes})
    else:
        return render(request, 'countmanagement.html',
                      {'title': title, 'account': account, 'count': count, 'nowss': now_time, 'user': user, 'admin_flog': admin_flog})


# 修改账户记录数据
def edit_count(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    if request.method == 'POST':
        errs = ''
        ids = request.POST.get('id')
        start_moneys = request.POST.get('start_money')
        end_moneys = request.POST.get('end_money')
        try:
            float(start_moneys)
            float(end_moneys)
        except ValueError:
            errs = '初始资金和结余资金必须为数字'
        if errs == '':
            operators = Userinfo.objects.get(username=user, deletes=False)
            last_date = Account_record.objects.filter(id=ids).get()
            account_names = last_date.account_name
            Account_record.objects.filter(id=ids).delete()
            if request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             start_money_img=last_date.start_money_img,
                                                             end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             start_money_img=last_date.start_money_img,
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             end_money_img=last_date.end_money_img, deletes=False)
            else:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            new_date = Account_record.objects.filter(id=ids).get()

            operation_types = '修改账户记录数据'
            before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s}' % (
                ids, last_date.account_name.account_name, last_date.start_money, last_date.end_money, last_date.operator, last_date.makes,
                last_date.start_money_img,
                last_date.end_money_img,)
            after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s}' % (
                new_date.id, account_names.account_name, start_moneys, end_moneys, user, new_date.start_money_img, new_date.end_money_img)
            Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations,
                               after_operation=after_operations)
            return redirect(to=countmanagement)
        else:
            title = '账户记录管理'
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            dates = get_nday_list2(2, now_time)
            account = Brank_account.objects.filter(brank_operator__username=user, deletes=False).all()
            count = Account_record.objects.filter(datess__gte=dates, deletes=False).all()
            forms = Forms()
            edit_form = Edit_forms()
            return render(request, 'countmanagement2.html',
                          {'title': title, 'account': account, 'count': count, 'nowss': now_time, 'formm': forms, 'edit_form': edit_form,
                           'errs': errs, 'user': user})
    current_data = Account_record.objects.filter(id=ids).get()
    msg = json.dumps(
        {'account_name': current_data.account_name.account_name, 'start_money': current_data.start_money, 'end_money': current_data.end_money,
         'ids': current_data.id})
    return HttpResponse(msg)


# 删除账户记录数据
def deletes_count(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    Account_record.objects.filter(id=ids).update(deletes='True')
    last_date = Account_record.objects.get(id=ids)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除账户记录数据'
    before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s}' % (
        ids, last_date.account_name, last_date.start_money, last_date.end_money, last_date.operator, last_date.makes, last_date.start_money_img,
        last_date.end_money_img,)
    after_operations = '删除了id=%s账户记录数据' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return redirect('/countmanagement/')


# 添加喝酒数据
def brushmanagement(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '喝酒'
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    # tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator=user, deletes='False')[::-1]
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=user, deletes='False')[::-1]
    add_brush_form = Add_brush_data()
    edit_brush_form = Edit_brush_data()
    errs = ''
    if request.method == 'POST':
        shopnames = request.POST.get('shopname')
        qq_or_weixins = request.POST.get('qq_or_weixin')
        qq_or_weixins = str(qq_or_weixins).strip()
        wang_wang_numbers = request.POST.get('wang_wang_number')
        wang_wang_numbers = str(wang_wang_numbers).strip()
        online_order_numbers = request.POST.get('online_order_number')
        online_order_numbers = online_order_numbers.strip()
        transaction_datas = request.POST.get('transaction_data')
        payment_types = request.POST.get('payment_type')
        payment_amounts = request.POST.get('payment_amount')
        payment_accounts = request.POST.get('payment_account')
        operators = Userinfo.objects.get(username=user, deletes=False)
        remarkss = request.POST.get('remarks')
        if payment_accounts == None:
            errs = '账户名不能为空'
        else:
            # 验证付款金额是否为float类型
            try:
                float(payment_amounts)
            except ValueError:
                errs = '付款金额必须为数字'
            onlys = Brush_single_entry.objects.filter(online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                                      payment_type=payment_types, deletes=False).all()
            if onlys:
                errs = '该订单记录已存在'
            if len(online_order_numbers) != 18:
                errs = '线上订单号格式错误'
        if errs == '':
            Brush_single_entry.objects.create(shopname=shopnames, qq_or_weixin=qq_or_weixins, wang_wang_number=wang_wang_numbers,
                                              online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                              payment_type=payment_types, payment_amount=payment_amounts,
                                              payment_account=Brank_account.objects.get(account_name=payment_accounts, deletes=False),
                                              operator=operators, remarks=remarkss, deletes=False)
            if Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts):
                Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts).update(makes=False)
            last_table = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=user).last()
            last_add_time = t(last_table.add_time)
            operation_types = '创建喝酒数据'
            after_operations = '{id：%s，店铺名：%s，旺旺号：%s，线上订单号：%s，成交日期：%s，付款类型：%s，付款金额：%s，付款账户：%s，操作员：%s，备注：%s}' % (
                last_table.id, shopnames, wang_wang_numbers, online_order_numbers, transaction_datas, payment_types, payment_amounts,
                payment_accounts, user, remarkss)
            Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
            msg = json.dumps(
                {'id': last_table.id, 'shopname': shopnames, 'wang_wang_number': wang_wang_numbers, 'online_order_number': online_order_numbers,
                 'transaction_data': transaction_datas, 'payment_type': payment_types, 'payment_amount': payment_amounts,
                 'payment_account': payment_accounts, 'remarks': remarkss, 'add_time': last_add_time, 'qq_or_weixin': qq_or_weixins})
            return HttpResponse(msg)
        else:
            return HttpResponse(json.dumps({'err': errs}))
    reminds = ''
    unmakes = 0
    makes = 0
    for i in account:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    return render(request, 'brush2.html',
                  {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables, 'add_brush_form': add_brush_form,
                   'edit_brush_form': edit_brush_form, 'user': user, 'errs': errs, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes})


# 修改喝酒数据
def edit(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    errs = ''
    if request.method == 'POST':
        ids = request.POST.get('id')
        shopnames = request.POST.get('shopname')
        qq_or_weixins = request.POST.get('qq_or_weixin')
        qq_or_weixins = str(qq_or_weixins).strip()
        wang_wang_numbers = request.POST.get('wang_wang_number')
        wang_wang_numbers = str(wang_wang_numbers).strip()
        online_order_numbers = request.POST.get('online_order_number')
        transaction_datas = request.POST.get('transaction_data')
        payment_types = request.POST.get('payment_type')
        payment_amounts = request.POST.get('payment_amount')
        payment_accounts = request.POST.get('payment_account')
        remarkss = request.POST.get('remarks')
        operators = Userinfo.objects.get(username=user, deletes=False)
        try:
            float(payment_amounts)
        except ValueError:
            errs = '付款金额必须为数字'
        if errs == '':
            add_time = datetime.datetime.now()
            last_date = Brush_single_entry.objects.filter(id=ids).get()
            Brush_single_entry.objects.filter(id=ids).update(shopname=shopnames, qq_or_weixin=qq_or_weixins, wang_wang_number=wang_wang_numbers,
                                                             online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                                             payment_type=payment_types, payment_amount=payment_amounts,
                                                             payment_account=Brank_account.objects.get(account_name=payment_accounts, deletes=False),
                                                             remarks=remarkss, deletes=False)
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            if Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts):
                Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts).update(makes=False)

            operation_types = '修改喝酒数据'
            before_operations = '{id：%s，店铺名：%s，旺旺号：%s，线上订单号：%s，成交日期：%s，付款类型：%s，付款金额：%s，付款账户：%s，操作员：%s，备注：%s}' % (
                ids, last_date.shopname, last_date.wang_wang_number, last_date.online_order_number, last_date.transaction_data,
                last_date.payment_type,
                last_date.payment_amount, last_date.payment_account, user, last_date.remarks)
            after_operations = '{id：%s，店铺名：%s，旺旺号：%s，线上订单号：%s，成交日期：%s，付款类型：%s，付款金额：%s，付款账户：%s，操作员：%s，备注：%s}' % (
                ids, shopnames, wang_wang_numbers, online_order_numbers, transaction_datas, payment_types, payment_amounts, payment_accounts, user,
                remarkss)
            Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations,
                               after_operation=after_operations)
            return redirect(to=brushmanagement)
        else:
            title = '喝酒'
            account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
            shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator=operators, deletes='False')[::-1]
            add_brush_form = Add_brush_data()
            edit_brush_form = Edit_brush_data()
            return render(request, 'brush2.html',
                          {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables,
                           'add_brush_form': add_brush_form, 'edit_brush_form': edit_brush_form, 'user': user, 'errs': errs})
    current_data = Brush_single_entry.objects.filter(id=ids).get()
    msg = json.dumps({'ids': current_data.id, 'shopname': current_data.shopname, 'qq_or_weixin': current_data.qq_or_weixin,
                      'wang_wang_number': current_data.wang_wang_number, 'online_order_number': current_data.online_order_number,
                      'transaction_data': current_data.transaction_data, 'payment_type': current_data.payment_type,
                      'payment_amount': current_data.payment_amount, 'payment_account': current_data.payment_account.account_name,
                      'remarks': current_data.remarks, })
    return HttpResponse(msg)


# 删除喝酒数据
def delete_data(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    Brush_single_entry.objects.filter(id=ids).update(deletes='True', add_time=datetime.datetime.now())
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    payment_accounts = Brush_single_entry.objects.get(ids)
    if Account_record.objects.filter(datess__date=now_time, account_name=payment_accounts.payment_account):
        Account_record.objects.filter(datess__date=now_time, account_name=payment_accounts.payment_account).update(makes=False)
    last_date = Brush_single_entry.objects.filter(id=ids).get()
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除喝酒数据'
    before_operations = '{id：%s，店铺名：%s，旺旺号：%s，线上订单号：%s，成交日期：%s，付款类型：%s，付款金额：%s，付款账户：%s，操作员：%s，备注：%s}' % (
        ids, last_date.shopname, last_date.wang_wang_number, last_date.online_order_number, last_date.transaction_data, last_date.payment_type,
        last_date.payment_amount, last_date.payment_account, user, last_date.remarks)
    after_operations = '删除了id=%s喝酒数据' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return HttpResponse('od')


# 更多数据页面
def more_date(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '更多数据'
    userss = user
    operators = userss
    all_user = Userinfo.objects.filter(deletes=False).values('username').all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    shopss = 'alls'
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=userss, deletes='False').order_by('add_time')
    if request.method == 'POST':
        operators = request.POST.get('operator')
        shopss = request.POST.get('shopname')
        now_time = request.POST.get('add_time')
        if shopss == 'alls' and operators == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, deletes='False').order_by('add_time')
        elif shopss == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=operators, deletes='False').order_by(
                'add_time')
        else:
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shopss, deletes='False').order_by(
                'add_time')
    rouse = request.session.get('rouse')
    accountss = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    reminds = ''
    unmakes = 0
    makes = 0
    for i in accountss:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name=i.id, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name=i.id, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    if rouse == '运营':
        return render(request, 'more_data2.html',
                      {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables, 'all_user': all_user,
                       'operators': operators, 'userss': userss, 'shop_select': shopss, 'user': user, 'reminds': reminds, 'makes': makes,
                       'unmakes': unmakes})
    else:
        return render(request, 'more_data.html',
                      {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables, 'all_user': all_user,
                       'operators': operators, 'userss': userss, 'shop_select': shopss, 'user': user, 'admin_flog': admin_flog})


# 更多页面加载店铺名
def chose_shop(request):
    user = request.session.get('username')
    users = request.GET.get('operator')
    if users == '全部':
        shops = Shops.objects.filter(deletes='False').values_list('shopname').all()
        shops = [i for i in shops]
    else:
        shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
        shops = [i.shopname for i in shops]
    msg = json.dumps({'shops': shops})
    return HttpResponse(msg)


# 核对喝酒数据
def check_account(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '核对喝酒数据'
    errs = ''
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    accounts = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    edit_brush_form = Edit_brush_data()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    account = Brank_account.objects.filter(brank_operator__username=user,deletes=False).first()
    for i in accounts:
        account = i.id
        break

    if request.method == 'POST':
        now_time = request.POST.get('check_data')
        account = request.POST.get('payment_account')
        if account == None:
            errs = '请选择查询账户名'
            account = Brank_account.objects.filter(brank_operator__username=user, deletes=False).first()
        else:
            account = Brank_account.objects.get(account_name=account, deletes=False)
    if account:
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, payment_account=account, deletes='False').all()
    else:
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, deletes='False').all()
    pay_money = 0.0
    for table in tables:
        pay_money += float(table.payment_amount)
    account_data = Account_record.objects.filter(account_name=account, datess__date=now_time, deletes=False).all()
    if account_data:
        account_data = account_data.get()
        star_money_img = account_data.start_money_img
        end_money_img = account_data.end_money_img
        if star_money_img and end_money_img:
            actual_cost = float(account_data.start_money) - float(account_data.end_money)
        else:
            actual_cost = '该账户没有上传截图，无法核账'
    else:
        actual_cost = '没有当天的账户信息，无法核账'
    accountss = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    # 提示运营有账户未确认
    reminds = ''
    unmakes = 0
    makes = 0
    for i in accountss:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name=i.id, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name=i.id, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    return render(request, 'check_account2.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money,
                   'actual_cost': actual_cost, 'user': user, 'edit_brush_form': edit_brush_form, 'shops': shops, 'user': user,
                   'payment_account': account, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes,'errs':errs})


# 确认核对
def make_account(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    account = request.GET.get('payment_account')
    now_time = request.GET.get('check_data')
    Account_record.objects.filter(datess__date=now_time, account_name__account_name=account).update(makes=True)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '账户核对成功'
    after_operations = '{日期：%s，账户名：%s}' % (now_time, account)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
    return HttpResponse(json.dumps('确认成功'))


# 按日期查询账户记录
def search_count(request):
    search_date = request.GET.get('search_data')
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '账户记录管理'
    account = Brank_account.objects.all()
    forms = Forms()
    edit_form = Edit_forms()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    if search_date:
        count = Account_record.objects.filter(datess__date=search_date, deletes=False).all()
    else:
        search_date = now_time
        count = Account_record.objects.filter(datess__date=now_time, deletes=False).all()
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    if rouse == '财务':
        return render(request, 'countmanagement.html', {'title': title, 'account': account, 'count': count, 'nowss': search_date, 'user': user})
    else:
        return render(request, 'countmanagement2.html',
                      {'title': title, 'account': account, 'count': count, 'nowss': search_date, 'formm': forms, 'edit_form': edit_form,
                       'user': user, 'admin_flog': admin_flog})


# 账户账单
def account_bill(request):
    title = '账户账单'
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    account = Brank_account.objects.filter(deletes=False).first()
    count_stats = ''
    if account:
        account_names = account.account_name
        accounts = Brank_account.objects.filter(deletes=False).all()
        if request.method == 'POST':
            now_time = request.POST.get('check_data')
            account_names = request.POST.get('account_name')
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, payment_account__account_name=account_names, deletes=False).all()
        pay_money = 0
        for table in tables:
            pay_money += float(table.payment_amount)
        account_data = Account_record.objects.filter(account_name__account_name=account_names, datess__date=now_time, deletes=False)
        if account_data:
            account_data = account_data.get()
            star_money_img = account_data.start_money_img
            end_money_img = account_data.end_money_img
            if star_money_img and end_money_img:
                actual_cost = float(account_data.start_money) - float(account_data.end_money)
            else:
                actual_cost = '该账户没有上传截图'
            if account_data.makes == False:
                count_stats = '该账户已确认'
            else:
                count_stats = '该账户未确认'
        else:
            actual_cost = '没有当天的账户信息'
    else:
        accounts = ''
        account_names = ''
        pay_money = 0
        actual_cost = '没有银行账户'
        tables = Brush_single_entry.objects.all()
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'account_bill.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money,
                   'actual_cost': actual_cost, 'user': user, 'account_name': account_names, 'count_stats': count_stats, 'admin_flog': admin_flog})


# 店铺账单
def shop_bill(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '店铺账单'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_shop = Shops.objects.filter(deletes=False).first()
    if first_shop:
        shop_name = first_shop.shopname
    else:
        shop_name = ''
    accounts = Shops.objects.filter(deletes=False).all()
    if request.method == 'POST':
        now_time = request.POST.get('check_data')
        shop_name = request.POST.get('shop_name')
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shop_name, deletes=False).all()
    pay_money = 0
    for table in tables:
        pay_money += float(table.payment_amount)
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=True, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'shop_bill.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money, 'user': user,
                   'shop_name': shop_name, 'admin_flog': admin_flog})
