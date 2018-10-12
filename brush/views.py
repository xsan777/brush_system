from django.shortcuts import render, HttpResponse, redirect
from brush.models import *
import time, json, datetime
from .forms import *
import django_excel as excel


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


# 获取前n天的日期
def get_nday_list2(n, now_time):
    dd = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    before_n_days2 = []
    for i in range(1, n + 1)[::-1]:
        bb = str(dd - datetime.timedelta(days=i - 1))
        aa = bb.replace(' 00:00:00', '')
        before_n_days2.append(aa)
    return before_n_days2[0]


# 获取下载的月份
def t_mouth(search_time):
    search_time = search_time.split('-')
    mouths = search_time[1]
    if mouths[0] == '0':
        return mouths[1]
    else:
        return mouths


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
                    return redirect(to=search_total_count)
        msg = '用户名或密码错误'
    return render(request, 'login.html', {'err_msg': msg})


# 修改密码
def update_passwd(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    passwds = request.POST.get('passwd')
    passwd2s = request.POST.get('passwd2')
    if passwds and passwd2s:
        if passwds == passwd2s:
            user_id = Userinfo.objects.get(username=user, deletes=False)
            Userinfo.objects.filter(username=user, deletes=False).update(passwd=passwds)
            msg = ''
            msg = json.dumps(msg)
            operators = Userinfo.objects.get(username=user, deletes=False)
            operation_types = '用户自己修改密码'
            before_operations = '{id：%d，用户名：%s，旧密码：%s，角色：%s，职位描述：%s，}' % (
                user_id.id, user_id.username, user_id.passwd, user_id.rouse, user_id.description,)
            after_operations = '{id：%s，用户名：%s，新密码：%s，角色：%s，职位描述：%s，}' % (
                user_id.id, user, passwds, rouse, user_id.description,)
            Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                               before_operation=before_operations)
        else:
            msg = '两次输入密码不一致，请重新修改'
            msg = json.dumps(msg)
        return HttpResponse(msg)


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
        total_accounts_list = request.POST.getlist('total_accounts')
        # 财务角色自动绑定所有店铺和所有总账户
        if rouses == '财务':
            shop_all = Shops.objects.filter(deletes=False).all()
            shop_list = []
            for j in shop_all:
                shop_list.append(j.shopname)
            total_account_all = Total_brank_account.objects.filter(deletes=False).all()
            total_accounts_list = []
            for m in total_account_all:
                total_accounts_list.append(m.total_account_name)
        if passwd2s == passwds:
            if len(shop_list) != 0:
                if len(total_accounts_list) != 0:
                    Userinfo.objects.create(username=usernames, passwd=passwds, rouse=rouses, description=descriptions, deletes=False)
                    user_ids = Userinfo.objects.filter(username=usernames, deletes=False).get()
                    # 将店铺与用户绑定
                    for shop in shop_list:
                        user_ids.shop.add(Shops.objects.get(shopname=shop, deletes=False))
                    # 将总账户与用户绑定
                    for accounts in total_accounts_list:
                        user_ids.total_brank_account.add(Total_brank_account.objects.get(total_account_name=accounts, deletes=False))
                    last_date = Userinfo.objects.last()
                    shops_clean = last_date.shop.all()
                    shops = ''
                    for user_shop in shops_clean:
                        shops += str(user_shop)
                        shops += '、'
                    total_account_names = ''
                    for total in total_accounts_list:
                        total_account_names += total
                        total_account_names += '、'
                    operators = Userinfo.objects.get(username=user, deletes=False)
                    operation_types = '创建新用户'
                    after_operations = '{id：%d，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s，使用总账户：%s}' % (
                        last_date.id, usernames, passwds, rouse, descriptions, shops, total_account_names)
                    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
                else:
                    msgs = '必须选择总账户'
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
        total_accounts = ''
        if i.rouse == '财务':
            total_accounts = '所有总账户'
        else:
            for user_total_accounts in i.total_brank_account.filter(deletes=False).all():
                total_accounts += str(user_total_accounts.total_account_name)
                total_accounts += '、'
        tables['total_accounts'] = total_accounts
        table_list.append(tables)
    shopss = Shops.objects.filter(deletes=False).all()
    total_account = Total_brank_account.objects.filter(deletes=False).all()
    add_form = Add_user()
    edit_form = Edit_user()

    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'user.html',
                  {'title': title, 'tables': table_list, 'shops': shopss, 'add_form': add_form, 'edit_user': edit_form, 'err_msg': err_msg,
                   'msgs': msgs, 'user': user, 'admin_flog': admin_flog, 'total_account': total_account, 'update_passwd': update_passwd})


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
        total_brank_account_list = request.POST.getlist('edit_total_brank_accounts')
        if rouses == '财务':
            shop_all = Shops.objects.filter(deletes=False).all()
            shop_list = []
            for j in shop_all:
                shop_list.append(j.shopname)
            total_accounts = Total_brank_account.objects.filter(deletes=False).all()
            total_brank_account_list = []
            for m in total_accounts:
                total_brank_account_list.append(m.total_account_name)
        if passwd2s == passwds:
            if len(shop_list) != 0:
                if len(total_brank_account_list) != 0:
                    user_id = Userinfo.objects.get(id=ids)
                    usernames = user_id.username
                    shops_clean = user_id.shop.filter(deletes=False).all()
                    before_shops = ''
                    for user_shop in shops_clean:
                        before_shops += str(user_shop)
                        before_shops += '、'
                    before_total_account = user_id.total_brank_account.filter(deletes=False).all()
                    before_total_accounts = ''
                    for total_account in before_total_account:
                        before_total_accounts += str(total_account.total_account_name)
                        before_total_accounts += '、'
                    Userinfo.objects.filter(id=ids).update(username=usernames, passwd=passwds, rouse=rouses, description=descriptions, deletes=False)
                    # 将用户与店铺绑定
                    user_id.shop.clear()
                    for shop in shop_list:
                        user_id.shop.add(Shops.objects.get(shopname=shop, deletes=False))
                    # 将用户与总账户绑定
                    user_id.total_brank_account.clear()
                    for total_brank_account in total_brank_account_list:
                        user_id.total_brank_account.add(Total_brank_account.objects.get(total_account_name=total_brank_account, deletes=False))

                    update_date = Userinfo.objects.get(id=ids)
                    shops_clean = update_date.shop.filter(deletes=False).all()
                    shops = ''
                    for user_shop in shops_clean:
                        shops += str(user_shop)
                        shops += '、'

                    after_total_account = update_date.total_brank_account.filter(deletes=False).all()
                    after_total_accounts = ''
                    for total_account in after_total_account:
                        after_total_accounts += str(total_account.total_account_name)
                        after_total_accounts += '、'
                    operators = Userinfo.objects.get(username=user, deletes=False)
                    operation_types = '修改用户信息'
                    before_operations = '{id：%d，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s，使用的总账户：%s}' % (
                        user_id.id, user_id.username, user_id.passwd, user_id.rouse, user_id.description, before_shops, before_total_accounts)
                    after_operations = '{id：%s，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s，使用的总账户：%s}' % (
                        ids, usernames, passwds, rouse, descriptions, shops, after_total_accounts)
                    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                                       before_operation=before_operations)
                else:
                    err_msg = '必须选择总账户'
            else:
                err_msg = '必须选择店铺'
    current_data = Userinfo.objects.filter(id=ids).get()
    msg = json.dumps(
        {'rose': current_data.rouse, 'username': current_data.username, 'passwd': current_data.passwd, 'description': current_data.description,
         'ids': current_data.id, 'err': err_msg, })
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
    total_brank_all = Total_brank_account.objects.filter(deletes=False).all()
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        total_brank_accounts = request.POST.get('total_brank_account')
        Shops.objects.create(shopname=shop_name, deletes=False,
                             own_total_brank=Total_brank_account.objects.get(total_account_name=total_brank_accounts, deletes=False))
        # 财务账号自动绑定新开店铺
        user_need = Userinfo.objects.filter(rouse='财务', deletes=False).all()
        for user_add in user_need:
            user_add.shop.add(Shops.objects.get(shopname=shop_name, deletes=False))

        last_date = Shops.objects.last()
        operation_types = '添加店铺'
        after_operations = '{id：%d，店铺名：%s，店铺总账户：%s}' % (last_date.id, shop_name, total_brank_accounts)
        Log.objects.create(operator=Userinfo.objects.get(username=user, deletes=False), operation_type=operation_types,
                           after_operation=after_operations)
    shop_info = []
    for shop in shop_all:
        tables = {}
        tables['shop_name'] = shop.shopname
        tables['id'] = shop.id
        owners = ''
        for owner in shop.userinfo_set.filter(rouse='运营', deletes=False).all():
            owners += str(owner.username)
            owners += '、'
        tables['shop_owners'] = owners
        tables['own_total_brank'] = shop.own_total_brank.total_account_name
        shop_info.append(tables)
    add_shop_form = Add_shop_form()
    edit_shop_form = Edit_shop_form()
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'shops.html',
                  {'title': title, 'tables': shop_info, 'add_shop_form': add_shop_form, 'edit_shop_form': edit_shop_form, 'user': user,
                   'admin_flog': admin_flog, 'total_brank_all': total_brank_all, 'update_passwd': update_passwd})


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
        total_account_names = request.POST.get('edit_total_account_name')
        before_shop = Shops.objects.get(id=ids)
        Shops.objects.filter(id=ids).update(own_total_brank=Total_brank_account.objects.get(total_account_name=total_account_names, deletes=False))
        operators = Userinfo.objects.get(username=user, deletes=False)
        operation_types = '修改店铺信息'
        before_operations = '{id：%s，店铺名：%s，总账户名：%s}' % (ids, before_shop.shopname, before_shop.own_total_brank.total_account_name)
        after_operations = '{id：%s，店铺名：%s，总账户名：%s}' % (ids, before_shop.shopname, total_account_names)
        Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations, after_operation=after_operations)
        return redirect(to=shopmanagement)
    before_shop = Shops.objects.get(id=ids)
    msg = json.dumps({'ids': ids, 'shopname': before_shop.shopname})
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


# 总账户管理
def total_brank_management(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    title = '总账户管理'
    msg = ''
    if request.method == 'POST':
        now_time = time.strftime('%Y-%m-%d', time.localtime())
        total_account_names = request.POST.get('total_brank_account_name')
        total_brank_names = request.POST.get('brank_name')
        total_brank_numbers = request.POST.get('brank_number')
        total_brank_card_numbers = request.POST.get('brank_card_number')
        total_brank_account_name_exit = Total_brank_account.objects.filter(total_account_name=total_account_names, deletes=False).all()
        total_brank_card_number_exit = Total_brank_account.objects.filter(total_brank_card_number=total_brank_card_numbers, deletes=False).all()
        if len(total_brank_account_name_exit) == 0:
            if len(total_brank_card_number_exit) == 0:
                Total_brank_account.objects.create(datess=now_time, total_brank_card_number=total_brank_card_numbers,
                                                   total_brank_name=total_brank_names, total_brank_number=total_brank_numbers,
                                                   total_account_name=total_account_names, deletes=False)
                # 财务账号自动绑定添加的总账户
                user_need = Userinfo.objects.filter(rouse='财务', deletes=False).all()
                for user_add in user_need:
                    user_add.total_brank_account.add(Total_brank_account.objects.get(total_account_name=total_account_names, deletes=False))
                last_total_account = Total_brank_account.objects.filter(deletes=False).last()
                operation_types = '创建总账户'
                after_operations = '{id：%d，总账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，}' % (
                    last_total_account.id, total_account_names, total_brank_names, total_brank_numbers, total_brank_card_numbers,)
                Log.objects.create(operator=Userinfo.objects.get(username=user, deletes=False), operation_type=operation_types,
                                   after_operation=after_operations)
            else:
                msg = '该总账户卡号已存在'
        else:
            msg = '该总账户名已存在'
    account_names = request.GET.get('account_name')
    if account_names:
        tables = Total_brank_account.objects.filter(total_account_name=account_names, deletes=False).all()
    else:
        tables = Total_brank_account.objects.filter(deletes=False).all()
    table_list = []
    for i in tables:
        tables = {}
        tables['id'] = i.id
        tables['account_name'] = i.total_account_name
        tables['brank_name'] = i.total_brank_name
        tables['brank_card_number'] = i.total_brank_card_number
        tables['brank_number'] = i.total_brank_number
        own_shops = ''
        for own_shop in i.shops_set.filter(deletes=False).all():
            own_shops += str(own_shop.shopname)
            own_shops += '、'
        tables['shop_owner'] = own_shops
        owers = ''
        for ower in i.userinfo_set.filter(rouse='运营', deletes=False).all():
            owers += str(ower.username)
            owers += '、'
        tables['owers'] = owers
        table_list.append(tables)
    add_total_brank_form = Total_brank_account_form()
    edit_total_brank_form = Edit_total_brank_account_form()

    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'total_brankmanagement.html',
                  {'title': title, 'tables': table_list, 'add_total_brank_form': add_total_brank_form, 'msg': msg,
                   'edit_total_brank_form': edit_total_brank_form, 'user': user, 'admin_flog': admin_flog, 'update_passwd': update_passwd})


# 验证总账户名
def verification_total_account(request):
    total_account_names = request.GET.get('total_account_name')
    total_brank_card_nums = request.GET.get('total_brank_card_num')
    exit_total_account = Total_brank_account.objects.filter(total_account_name=total_account_names, deletes=False).all()
    # exit_total_brank_card_nums = Total_brank_account.objects.filter(total_brank_card_number=total_brank_card_nums, deletes=False).all()
    if len(exit_total_account) == 0:
        msg = ''
    else:
        msg = '该总账户名存在'
    return HttpResponse(json.dumps(msg))


# 修改总账户
def edit_total_brank(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    if request.method == 'POST':
        total_account_names = request.POST.get('total_brank_account_name')
        total_brank_names = request.POST.get('brank_name')
        total_brank_numbers = request.POST.get('brank_number')
        total_brank_card_numbers = request.POST.get('brank_card_number')
        ids = request.POST.get('id')
        last_data = Total_brank_account.objects.get(id=ids)
        before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，}' % (
            ids, last_data.total_account_name, last_data.total_brank_name, last_data.total_brank_number, last_data.total_brank_card_number,)
        Total_brank_account.objects.filter(id=ids).update(total_brank_name=total_brank_names, total_brank_number=total_brank_numbers,
                                                          total_brank_card_number=total_brank_card_numbers)
        operation_types = '修改总账户'
        operators = Userinfo.objects.get(username=user, deletes=False)
        after_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s}' % (
            ids, total_account_names, total_brank_names, total_brank_numbers, total_brank_card_numbers,)
        Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                           before_operation=before_operations)
        return redirect(to=total_brank_management)
    current_data = Total_brank_account.objects.get(id=ids)
    msg = {'total_brank_name': current_data.total_brank_name, 'total_account_name': current_data.total_account_name,
           'total_brank_num': current_data.total_brank_number, 'total_brank_card_num': current_data.total_brank_card_number, 'ids': ids}
    return HttpResponse(json.dumps(msg))


# 删除总账户
def del_total_brank(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    if rouse == '运营':
        return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
    ids = request.GET.get('id')
    Total_brank_account.objects.filter(id=ids).update(deletes='True')
    total_brank_card_id = Total_brank_account.objects.filter(id=ids).get()
    before_operation_lists = ''
    for before_operations in total_brank_card_id.userinfo_set.filter(deletes=False).all():
        before_operation_lists += str(before_operations.username)
        before_operation_lists += '、'
    before_shop_list = ''
    for before_shops in total_brank_card_id.shops_set.filter(deletes=False).all():
        before_shop_list += str(before_shops.shopname)
        before_shop_list += '、'
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除总账户'
    before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，总账户使用人：%s，绑定店铺：%s}' % (
        ids, total_brank_card_id.total_account_name, total_brank_card_id.total_brank_name, total_brank_card_id.total_brank_number,
        total_brank_card_id.total_brank_card_number, before_operation_lists, before_shop_list)
    after_operations = '删除了总账户{id：%s，账户名：%s}' % (ids, total_brank_card_id.total_account_name)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return HttpResponse('ok')


# 子银行账户管理
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
    user_list = Userinfo.objects.filter(rouse='运营', deletes=False).all()
    total_accounts = Total_brank_account.objects.filter(deletes=False).all()
    add_brank_account_form = Add_brank_account()
    edit_brank_account_form = Edit_brank_account()
    msg = ''
    if request.method == 'POST':
        account_names = request.POST.get('account_name')
        brank_names = request.POST.get('brank_name')
        brank_numbers = request.POST.get('brank_number')
        brank_card_numbers = request.POST.get('brank_card_number')
        total_account_of = request.POST.get('total_account')
        brank_operator_list = request.POST.getlist('checkitem')
        if total_account_of != None:
            if len(brank_operator_list) != 0:
                Brank_account.objects.create(account_name=account_names, brank_name=brank_names, brank_number=brank_numbers,
                                             brank_card_number=brank_card_numbers, deletes=False,
                                             total_account_name=Total_brank_account.objects.get(total_account_name=total_account_of, deletes=False))
                brank_card_id = Brank_account.objects.filter(account_name=account_names, deletes=False).get()
                for users in brank_operator_list:
                    brank_card_id.brank_operator.add(Userinfo.objects.get(username=users, deletes=False))
                user_clean = brank_card_id.brank_operator.all()
                brank_operator_lists = ''
                for user_brank in user_clean:
                    brank_operator_lists += str(user_brank.username)
                    brank_operator_lists += '、'
                operation_types = '创建银行账户'
                after_operations = '{id：%d，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，所属总账户：%s，银行卡操作人：%s}' % (
                    brank_card_id.id, account_names, brank_names, brank_numbers, brank_card_numbers, total_account_of, brank_operator_lists)
                Log.objects.create(operator=Userinfo.objects.get(username=user, deletes=False), operation_type=operation_types,
                                   after_operation=after_operations)
            else:
                msg = '必须选择银行卡使用人'
        else:
            msg = '必须选择所属总账户'
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
        tables['total_account_name'] = i.total_account_name.total_account_name
        table_list.append(tables)
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'brankmanagement.html',
                  {'title': title, 'tables': table_list, 'add_brank_account_form': add_brank_account_form, 'user_list': user_list, 'msg': msg,
                   'edit_brank_account_form': edit_brank_account_form, 'user': user, 'admin_flog': admin_flog, 'total_accounts': total_accounts,
                   'update_passwd': update_passwd})


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

        brank_names = request.POST.get('brank_name')
        brank_numbers = request.POST.get('brank_number')
        brank_card_numbers = request.POST.get('brank_card_number')
        total_account_names = request.POST.get('edit_total_account_name')
        brank_operator_list = request.POST.getlist('checkitem')
        if len(brank_operator_list) != 0:
            if len(total_account_names) != 0:
                brank_card_id = Brank_account.objects.get(id=ids)
                account_names = brank_card_id.account_name
                before_operation_lists = ''
                for before_operations in brank_card_id.brank_operator.all():
                    before_operation_lists += str(before_operations.username)
                    before_operation_lists += '、'
                before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，所属账户：%s，银行卡操作人：%s}' % (
                    ids, brank_card_id.account_name, brank_card_id.brank_name, brank_card_id.brank_number, brank_card_id.brank_card_number,
                    brank_card_id.total_account_name.total_account_name, before_operation_lists)
                Brank_account.objects.filter(id=ids).update(brank_name=brank_names, brank_number=brank_numbers,
                                                            brank_card_number=brank_card_numbers, deletes=False,
                                                            total_account_name=Total_brank_account.objects.get(total_account_name=total_account_names,
                                                                                                               deletes=False))
                brank_card_id2 = Brank_account.objects.filter(account_name=brank_card_id.account_name, deletes=False).get()
                brank_card_id2.brank_operator.clear()
                for users in brank_operator_list:
                    brank_card_id2.brank_operator.add(Userinfo.objects.get(username=users, deletes=False))
                user_clean = brank_card_id2.brank_operator.all()
                brank_operator_lists = ''
                for user_brank in user_clean:
                    brank_operator_lists += str(user_brank.username)
                    brank_operator_lists += '、'
                operation_types = '修改银行账户'
                operators = Userinfo.objects.get(username=user, deletes=False)
                after_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，所属账户：%s，银行卡操作人：%s}' % (
                    ids, account_names, brank_names, brank_numbers, brank_card_numbers, total_account_names, brank_operator_lists)
                Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                                   before_operation=before_operations)
            else:
                msgss = '必须选择所属总账户'
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
    before_operations = '{id：%s，账户名：%s，银行名：%s，开户行号：%s，银行卡号：%s，所属总账户：%s，银行卡操作人：%s}' % (
        ids, brank_card_id.account_name, brank_card_id.brank_name, brank_card_id.brank_number, brank_card_id.brank_card_number,
        brank_card_id.total_account_name, before_operation_lists)
    after_operations = '删除了id=%s的银行账户' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return HttpResponse('ok')


# 总账户记录管理
def total_countmanagement(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '总账户记录管理'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    add_times = datetime.datetime.now()
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account = user_total_account.total_brank_account.filter(deletes=False).all()
    if rouse == '财务':
        count = Total_account_record.objects.filter(datess__date=now_time, deletes=False).all()
    else:
        count = Total_account_record.objects.filter(datess__date=now_time, operator__username=user, deletes=False).all()
    forms = Forms()
    edit_form = Edit_forms()
    errs = ''
    if request.method == 'POST':
        account_names = request.POST.get('total_account_name')
        if account_names == '':
            errs = '总账户名不能为空'
        else:
            exits = Total_account_record.objects.filter(datess__gte=now_time, account_name__total_account_name=account_names, deletes=False).all()
            if len(exits) == 0:
                operators = Userinfo.objects.get(username=user, deletes=False)
                start_moneys = request.POST.get('start_money')
                end_moneys = request.POST.get('end_money')
                try:
                    float(start_moneys)
                    float(end_moneys)
                    errs = ''
                except ValueError:
                    errs = '初始资金和结余资金必须为数字'
                if errs == '':
                    account_names = Total_brank_account.objects.get(total_account_name=account_names, deletes=False)
                    Total_account_record.objects.create(datess=add_times, account_name=account_names, start_money=start_moneys,
                                                        end_money=end_moneys, operator=operators, makes='False',
                                                        start_money_img=request.FILES.get('start_money_img'),
                                                        end_money_img=request.FILES.get('end_money_img'), deletes=False)
                    last_date = Total_account_record.objects.last()
                    operation_types = '创建总账户记录'
                    after_operations = '{id：%s，总账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s}' % (
                        last_date.id, account_names.total_account_name, start_moneys, end_moneys, user, last_date.start_money_img,
                        last_date.end_money_img)
                    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
            else:
                errs = '该账户今日已创建记录'
    count_list = []
    for i in count:
        count_row = {}
        last_date = get_nday_list2(2, now_time)
        last_date_end_img = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
            'end_money_img')
        if len(last_date_end_img) > 0:
            last_date_end_img = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
                'end_money_img').get()
            count_row['last_date_end_img'] = last_date_end_img['end_money_img']
        else:
            count_row['last_date_end_img'] = '前一日无截图'
        # print(count_row['last_date_end_img'])
        count_row['id'] = i.id
        count_row['datess'] = i.datess
        count_row['account_name'] = i.account_name
        count_row['start_money'] = i.start_money
        count_row['end_money'] = i.end_money
        count_row['start_money_img'] = i.start_money_img
        count_row['end_money_img'] = i.end_money_img
        count_row['operator'] = i.operator.username
        count_row['makes'] = i.makes
        count_list.append(count_row)
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    account_unmakes = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account_unmakes:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                      deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                          deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'

    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time1 = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time1, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    if rouse == '运营':
        return render(request, 'total_countmanagement2.html',
                      {'title': title, 'total_account_all': account, 'count': count_list, 'nowss': now_time, 'formm': forms, 'edit_form': edit_form,
                       'errs': errs, 'update_passwd': update_passwd,
                       'user': user, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes, 'total_reminds': total_reminds})
    else:

        return render(request, 'countmanagement.html',
                      {'title': title, 'account': account, 'count': count, 'nowss': now_time1, 'user': user, 'admin_flog': admin_flog,
                       'update_passwd': update_passwd})


# 修改总账户记录数据
def edit_total_count(request):
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
            last_date = Total_account_record.objects.filter(id=ids).get()
            account_names = last_date.account_name
            before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s}' % (
                ids, last_date.account_name.total_account_name, last_date.start_money, last_date.end_money, last_date.operator.username,
                last_date.makes,
                last_date.start_money_img,
                last_date.end_money_img,)
            Total_account_record.objects.filter(id=ids).delete()
            if request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None:
                Total_account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names,
                                                                   start_money=start_moneys,
                                                                   end_money=end_moneys, operator=operators, makes='False',
                                                                   start_money_img=last_date.start_money_img,
                                                                   end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None:
                Total_account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names,
                                                                   start_money=start_moneys,
                                                                   end_money=end_moneys, operator=operators, makes='False',
                                                                   start_money_img=last_date.start_money_img,
                                                                   end_money_img=request.FILES.get('end_money_img'), deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None:
                Total_account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names,
                                                                   start_money=start_moneys,
                                                                   end_money=end_moneys, operator=operators, makes='False',
                                                                   start_money_img=request.FILES.get('start_money_img'),
                                                                   end_money_img=last_date.end_money_img, deletes=False)
            else:
                Total_account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names,
                                                                   start_money=start_moneys,
                                                                   end_money=end_moneys, operator=operators, makes='False',
                                                                   start_money_img=request.FILES.get('start_money_img'),
                                                                   end_money_img=request.FILES.get('end_money_img'), deletes=False)
            new_date = Total_account_record.objects.filter(id=ids).get()
            operation_types = '修改总账户记录数据'
            after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作人：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s}' % (
                new_date.id, account_names.total_account_name, start_moneys, end_moneys, user, new_date.start_money_img, new_date.end_money_img)
            Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations,
                               after_operation=after_operations)
            return redirect(to=total_countmanagement)
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
    current_data = Total_account_record.objects.filter(id=ids).get()
    msg = json.dumps(
        {'account_name': current_data.account_name.total_account_name, 'start_money': current_data.start_money, 'end_money': current_data.end_money,
         'ids': current_data.id})
    return HttpResponse(msg)


# 删除总账户记录
def delete_total_count(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    Total_account_record.objects.filter(id=ids).update(deletes='True')
    last_date = Total_account_record.objects.get(id=ids)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除账户记录数据'
    before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s}' % (
        ids, last_date.account_name.total_account_name, last_date.start_money, last_date.end_money, last_date.operator.username, last_date.makes,
        last_date.start_money_img,
        last_date.end_money_img,)
    after_operations = '删除了id=%s账户记录数据' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return redirect(to=total_countmanagement)


# 子账户记录管理
def countmanagement(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '账户记录管理'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    add_times = datetime.datetime.now()
    account = Brank_account.objects.filter(brank_operator__username=user, deletes=False).all()

    forms = Forms()
    edit_form = Edit_forms()
    errs = ''
    if request.method == 'POST':
        account_names = request.POST.get('account_name')
        if account_names == None:
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
                    weixin_withdraw_moneys = data['weixin_withdraw_money']
                    try:
                        start_moneys_float = float(start_moneys)
                        float(end_moneys)
                        float(weixin_withdraw_moneys)
                        errs = ''
                    except ValueError:
                        errs = '初始资金和结余资金和微信提现费用必须为数字'
                    if errs == '':
                        account_names = Brank_account.objects.get(account_name=account_names, deletes=False)
                        last_record = Account_record.objects.filter(account_name=account_names, deletes=False).last()
                        last_end_moneys = float(last_record.end_money)
                        start_moneys = last_end_moneys + start_moneys_float
                        start_moneys = '%.2f' % start_moneys
                        Account_record.objects.create(datess=add_times, account_name=account_names, start_money=start_moneys, end_money=end_moneys,
                                                      weixin_withdraw_money=weixin_withdraw_moneys, operator=operators, makes='False',
                                                      start_money_img=request.FILES.get('start_money_img'),
                                                      end_money_img=request.FILES.get('end_money_img'), weixin_img=request.FILES.get(
                                'weixin_img'), deletes=False)
                        last_date = Account_record.objects.last()
                        operation_types = '创建子账户记录'
                        after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}' % (
                            last_date.id, account_names.account_name, start_moneys, end_moneys, weixin_withdraw_moneys, user,
                            last_date.start_money_img,
                            last_date.end_money_img, last_date.weixin_img)
                        Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
            else:
                errs = '该账户今日已创建记录'
    if rouse == '财务':
        count = Account_record.objects.filter(datess__date=get_nday_list2(2, now_time), deletes=False).all()
    else:
        count = Account_record.objects.filter(datess__date=now_time, operator__username=user, deletes=False).all()
    count_list = []
    for i in count:
        count_row = {}
        last_end_money = Account_record.objects.filter( account_name=i.account_name, deletes=False).values(
            'end_money')
        if len(last_end_money) > 0:
            last_end_money = Account_record.objects.filter(account_name=i.account_name, deletes=False).values(
                'end_money').order_by('-datess')[1]
            count_row['last_end_money'] = last_end_money['end_money']
        else:
            count_row['last_end_money'] = '没有上次结余金额'
        count_row['id'] = i.id
        count_row['datess'] = i.datess
        count_row['account_name'] = i.account_name
        count_row['start_money'] = i.start_money
        count_row['end_money'] = i.end_money
        count_row['weixin_withdraw_money'] = i.weixin_withdraw_money
        count_row['start_money_img'] = i.start_money_img
        count_row['end_money_img'] = i.end_money_img
        count_row['weixin_img'] = i.weixin_img
        count_row['operator'] = i.operator
        count_row['makes'] = i.makes
        count_list.append(count_row)
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
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
    now_time1 = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time1, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    if rouse == '运营':
        return render(request, 'countmanagement2.html',
                      {'title': title, 'account': account, 'count': count_list, 'nowss': now_time, 'formm': forms, 'edit_form': edit_form,
                       'errs': errs,
                       'update_passwd': update_passwd,
                       'user': user, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes, 'total_reminds': total_reminds})
    else:
        return render(request, 'countmanagement.html',
                      {'title': title, 'account': account, 'count': count_list, 'nowss': now_time1, 'user': user, 'admin_flog': admin_flog,
                       'update_passwd': update_passwd})


# 修改子账户记录数据
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
        weixin_withdraw_moneys = request.POST.get('weixin_withdraw_money')
        try:
            float(start_moneys)
            float(end_moneys)
            float(weixin_withdraw_moneys)
        except ValueError:
            errs = '初始资金和结余资金和微信提现费用必须为数字'
        if errs == '':
            operators = Userinfo.objects.get(username=user, deletes=False)
            last_date = Account_record.objects.filter(id=ids).get()
            account_names = last_date.account_name
            Account_record.objects.filter(id=ids).delete()
            if request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys, start_money_img=last_date.start_money_img,
                                                             weixin_img=last_date.weixin_img, end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys, start_money_img=last_date.start_money_img,
                                                             weixin_img=last_date.weixin_img, end_money_img=request.FILES.get('end_money_img'),
                                                             deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'), weixin_img=last_date.weixin_img,
                                                             end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=last_date.start_money_img, weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=last_date.end_money_img, deletes=False)

            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'), weixin_img=last_date.weixin_img,
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=last_date.start_money_img,
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            else:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)

            # 修改总账户的状态
            new_date = Account_record.objects.filter(id=ids).get()
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            total_brank_names = new_date.account_name.total_account_name.total_account_name
            total_account_records = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names,
                                                                        deletes=False).all()
            if len(total_account_records) > 0:
                Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names, deletes=False).update(
                    makes=False)
            operation_types = '修改账户记录数据'
            before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}' % (
                ids, last_date.account_name.account_name, last_date.start_money, last_date.end_money, last_date.weixin_withdraw_money,
                last_date.operator.username, last_date.makes, last_date.start_money_img, last_date.end_money_img, last_date.weixin_img)
            after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}}' % (
                new_date.id, account_names.account_name, start_moneys, end_moneys, weixin_withdraw_moneys, user, new_date.start_money_img,
                new_date.end_money_img, new_date.weixin_img)
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
         'ids': current_data.id, 'weixin_withdraw_money': current_data.weixin_withdraw_money})
    return HttpResponse(msg)


# 通过总账户核对页面修改子账户记录数据
def edit_count_2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    if request.method == 'POST':
        errs = ''
        ids = request.POST.get('id')
        start_moneys = request.POST.get('start_money')
        end_moneys = request.POST.get('end_money')
        weixin_withdraw_moneys = request.POST.get('weixin_withdraw_money')
        try:
            float(start_moneys)
            float(end_moneys)
            float(weixin_withdraw_moneys)
        except ValueError:
            errs = '初始资金和结余资金和微信提现费用必须为数字'
        if errs == '':
            operators = Userinfo.objects.get(username=user, deletes=False)
            last_date = Account_record.objects.filter(id=ids).get()
            account_names = last_date.account_name
            Account_record.objects.filter(id=ids).delete()
            if request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys, start_money_img=last_date.start_money_img,
                                                             weixin_img=last_date.weixin_img, end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys, start_money_img=last_date.start_money_img,
                                                             weixin_img=last_date.weixin_img, end_money_img=request.FILES.get('end_money_img'),
                                                             deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'), weixin_img=last_date.weixin_img,
                                                             end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=last_date.start_money_img, weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=last_date.end_money_img, deletes=False)

            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') == None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'), weixin_img=last_date.weixin_img,
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            elif request.FILES.get('start_money_img') != None and request.FILES.get('end_money_img') == None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=last_date.end_money_img, deletes=False)
            elif request.FILES.get('start_money_img') == None and request.FILES.get('end_money_img') != None and request.FILES.get(
                    'weixin_img') != None:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=last_date.start_money_img,
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            else:
                Account_record.objects.filter(id=ids).create(id=ids, datess=last_date.datess, account_name=account_names, start_money=start_moneys,
                                                             end_money=end_moneys, operator=operators, makes='False',
                                                             weixin_withdraw_money=weixin_withdraw_moneys,
                                                             start_money_img=request.FILES.get('start_money_img'),
                                                             weixin_img=request.FILES.get('weixin_img'),
                                                             end_money_img=request.FILES.get('end_money_img'), deletes=False)
            # 修改总账户的状态
            new_date = Account_record.objects.filter(id=ids).get()
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            total_brank_names = new_date.account_name.total_account_name.total_account_name
            total_account_records = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names,
                                                                        deletes=False).all()
            if len(total_account_records) > 0:
                Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names, deletes=False).update(
                    makes=False)
            operation_types = '修改账户记录数据'
            before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}' % (
                ids, last_date.account_name.account_name, last_date.start_money, last_date.end_money, last_date.weixin_withdraw_money,
                last_date.operator.username, last_date.makes, last_date.start_money_img, last_date.end_money_img, last_date.weixin_img)
            after_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：False，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}}' % (
                new_date.id, account_names.account_name, start_moneys, end_moneys, weixin_withdraw_moneys, user, new_date.start_money_img,
                new_date.end_money_img, new_date.weixin_img)
            Log.objects.create(operator=operators, operation_type=operation_types, before_operation=before_operations,
                               after_operation=after_operations)
            return redirect(to=check_total_account)
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
         'ids': current_data.id, 'weixin_withdraw_money': current_data.weixin_withdraw_money})
    return HttpResponse(msg)


# 删除子账户记录数据
def deletes_count(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    ids = request.GET.get('id')
    Account_record.objects.filter(id=ids).update(deletes='True')
    last_date = Account_record.objects.get(id=ids)
    # 修改总账户的状态
    new_date = Account_record.objects.filter(id=ids).get()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    total_brank_names = new_date.account_name.total_account_name.total_account_name
    total_account_records = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names,
                                                                deletes=False).all()
    if len(total_account_records) > 0:
        Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names, deletes=False).update(
            makes=False)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除账户记录数据'
    before_operations = '{id：%s，账户名：%s，初始资金：%s，结余资金：%s，微信提现费用：%s，操作员：%s，运营确认：%s，初始资金截图：%s，结余资金截图：%s，微信提现费用截图：%s}' % (
        ids, last_date.account_name.account_name, last_date.start_money, last_date.end_money, last_date.weixin_withdraw_money,
        last_date.operator.username, last_date.makes, last_date.start_money_img, last_date.end_money_img, last_date.weixin_img)
    after_operations = '删除了id=%s账户记录数据' % (ids)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations, before_operation=before_operations)
    return redirect('/countmanagement/')


# 喝酒数据录入
def brushmanagement(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '喝酒'
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
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
        if online_order_numbers:
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
            # 验证线上订单号格式
            if online_order_numbers != '':
                if len(online_order_numbers) != 18:
                    errs = '线上订单号格式错误'
                else:
                    onlys = Brush_single_entry.objects.filter(online_order_number=online_order_numbers,
                                                              payment_type=payment_types, deletes=False).all()
                    if len(onlys) > 0:
                        errs = '该订单记录已存在'
        if errs == '':
            add_times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            Brush_single_entry.objects.create(shopname=shopnames, qq_or_weixin=qq_or_weixins, wang_wang_number=wang_wang_numbers,
                                              online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                              payment_type=payment_types, payment_amount=payment_amounts,
                                              payment_account=Brank_account.objects.get(account_name=payment_accounts, deletes=False),
                                              operator=operators, remarks=remarkss, deletes=False, add_time=add_times)
            if Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts, deletes=False):
                Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts, deletes=False).update(makes=False)
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
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    update_passwd = Updata_passwd()
    return render(request, 'brush2.html',
                  {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables, 'add_brush_form': add_brush_form,
                   'edit_brush_form': edit_brush_form, 'user': user, 'errs': errs, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes,
                   'total_reminds': total_reminds, 'update_passwd': update_passwd})


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
        if online_order_numbers != '':
            if len(online_order_numbers) != 18:
                errs = '线上订单号格式错误'
        if errs == '':
            last_date = Brush_single_entry.objects.filter(id=ids).get()
            Brush_single_entry.objects.filter(id=ids).update(shopname=shopnames, qq_or_weixin=qq_or_weixins, wang_wang_number=wang_wang_numbers,
                                                             online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                                             payment_type=payment_types, payment_amount=payment_amounts,
                                                             payment_account=Brank_account.objects.get(account_name=payment_accounts, deletes=False),
                                                             remarks=remarkss, deletes=False)
            now_time = time.strftime('%Y-%m-%d', time.localtime())
            # 修改子账户确认状态
            if Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts):
                Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts).update(makes=False)
            # 修改总账户确认状态
            total_brank_names = Brank_account.objects.get(account_name=payment_accounts, deletes=False).total_account_name.total_account_name
            total_account_records = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names,
                                                                        deletes=False).all()
            if len(total_account_records) > 0:
                Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names, deletes=False).update(
                    makes=False)
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

        return HttpResponse(json.dumps(errs))
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
    # 修改子账户确认状态
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    payment_accounts = Brush_single_entry.objects.get(id=ids)
    if Account_record.objects.filter(datess__date=now_time, account_name=payment_accounts.payment_account):
        Account_record.objects.filter(datess__date=now_time, account_name=payment_accounts.payment_account).update(makes=False)
    # 修改总账户确认状态
    total_brank_names = Brank_account.objects.get(account_name=payment_accounts.payment_account.account_name,
                                                  deletes=False).total_account_name.total_account_name
    total_account_records = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names,
                                                                deletes=False).all()
    if len(total_account_records) > 0:
        Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=total_brank_names, deletes=False).update(
            makes=False)
    last_date = Brush_single_entry.objects.filter(id=ids).get()
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '删除喝酒数据'
    before_operations = '{id：%s，店铺名：%s，旺旺号：%s，线上订单号：%s，成交日期：%s，付款类型：%s，付款金额：%s，付款账户：%s，操作员：%s，备注：%s}' % (
        ids, last_date.shopname, last_date.wang_wang_number, last_date.online_order_number, last_date.transaction_data, last_date.payment_type,
        last_date.payment_amount, last_date.payment_account.account_name, user, last_date.remarks)
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
    title = '喝酒数据查询'
    userss = user
    operators = userss
    first_shop = Userinfo.objects.filter(username=user, deletes=False).get().shop.filter(deletes=False).first()
    all_user = Shops.objects.filter(shopname=first_shop, deletes=False).get().userinfo_set.filter(rouse='运营', deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    shopss = 'alls'
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=userss, shopname=first_shop, deletes='False').order_by(
        'add_time')
    if request.method == 'POST':
        operators = request.POST.get('operator')
        shopss = request.POST.get('shopname')
        now_time = request.POST.get('add_time')
        if operators == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shopss, deletes='False').order_by('add_time')
        else:
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=operators, shopname=shopss,
                                                       deletes='False').order_by('add_time')

    accountss = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    reminds = ''
    unmakes = 0
    makes = 0
    for i in accountss:
        check_countss = Account_record.objects.filter(datess__date=now_time, account_name=i.id, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__date=now_time, account_name=i.id, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time3 = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time3, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    update_passwd = Updata_passwd()
    return render(request, 'more_data2.html',
                  {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables, 'all_user': all_user,
                   'operators': operators, 'userss': userss, 'shop_select': shopss, 'user': user, 'reminds': reminds, 'makes': makes,
                   'unmakes': unmakes, 'total_reminds': total_reminds, 'update_passwd': update_passwd})


# 更多页面加载操作人
def chose_operator(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    shops_ = request.GET.get('shopname')
    operators = Shops.objects.filter(shopname=shops_, deletes=False).get().userinfo_set.filter(rouse='运营', deletes=False).values_list(
        'username').all()
    operators = [i for i in operators]
    msg = json.dumps({'operators': operators})
    return HttpResponse(msg)


# 子账户核对
def check_account(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '核对喝酒数据'
    errs = ''
    actual_err = ''
    account_select = ''
    makes_stats = ''
    pay_money_all = ''
    actual_cost = ''
    weixin_withdraw_moneys = ''
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    accounts = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    edit_brush_form = Edit_brush_data()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    account = Brank_account.objects.filter(brank_operator__username=user, deletes=False).first()
    for i in accounts:
        account = i.id
        break
    if request.method == 'POST':
        now_time = request.POST.get('check_data')
        account = request.POST.get('payment_account')
        account_select = account
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
    un_online_order_number = 0
    handing_free_all = 0.00
    for table in tables:
        pay_money += float(table.payment_amount)
        # if table.online_order_number == '' and table.payment_type != '刮刮卡':
        if table.online_order_number == '':
            pay_type = table.payment_type
            if pay_type == '手续费' or pay_type == '买家秀' or pay_type == '快递费' or pay_type == '收藏、加购' or pay_type == '直通车点击':
                pass
            else:
                un_online_order_number += 1
        if table.payment_type == '手续费':
            handing_free_all += float(table.payment_amount)

    handing_free_all = '%.2f' % handing_free_all
    pay_money = '%.2f' % pay_money
    account_data = Account_record.objects.filter(account_name=account, datess__date=now_time, deletes=False).all()
    if account_data:
        account_data = account_data.get()
        weixin_withdraw_moneys = float(account_data.weixin_withdraw_money)
        # pay_money = float(pay_money)
        # pay_money_all = pay_money + weixin_withdraw_moneys
        pay_money_all = float(pay_money)
        star_money_img = account_data.start_money_img
        end_money_img = account_data.end_money_img
        weixin_img = account_data.weixin_img
        makes_stats = account_data.makes
        weixin_withdraw_moneys = '%.2f' % weixin_withdraw_moneys
        if star_money_img and end_money_img:
            if weixin_withdraw_moneys != '0.00' and weixin_img == '':
                actual_err = '该账户没有上传截图，无法核账'
            else:
                actual_cost = float(account_data.start_money) - float(account_data.end_money)
                actual_cost = '%.2f' % actual_cost
                # print(pay_money_all)
                pay_money_all = float(pay_money_all)
                pay_money_all = '%.2f' % pay_money_all
                if un_online_order_number != 0:
                    actual_err = '有' + str(un_online_order_number) + '条记录没有订单号'
                elif pay_money_all != actual_cost:
                    actual_err = '账目有问题，请仔细核对'
                elif weixin_withdraw_moneys != handing_free_all:
                    actual_err = '总手续费为' + handing_free_all + '，该账户记录提现费用为' + weixin_withdraw_moneys
        else:
            actual_err = '该账户缺少截图，无法核账'
    else:
        actual_err = '没有当天的账户信息，无法核账'
    accountss = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    # 提示运营有账户未确认
    reminds = ''
    unmakes = 0
    makes = 0
    for i in accountss:
        check_countss = Account_record.objects.filter(datess__date=now_time, account_name=i.id, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__date=now_time, account_name=i.id, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time3 = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time3, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    update_passwd = Updata_passwd()
    return render(request, 'check_account2.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money,
                   'actual_cost': actual_cost, 'user': user, 'edit_brush_form': edit_brush_form, 'shops': shops, 'user': user,
                   'payment_account': account, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes, 'errs': errs,
                   'total_reminds': total_reminds, 'update_passwd': update_passwd, 'actual_err': actual_err, 'makes_stats': makes_stats,
                   'account_select': account_select, 'pay_money_all': pay_money_all,
                   'weixin_withdraw_moneys': weixin_withdraw_moneys})


# 确认核对子账户
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


# 按日期查询子账户记录
def search_count(request):
    search_date = request.GET.get('search_data')
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '子账户记录管理'
    account = Brank_account.objects.all()
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account3 = user_total_account.brank_account_set.filter(deletes=False).all()
    forms = Forms()
    edit_form = Edit_forms()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    if search_date:
        now_time = search_date
        # count = Account_record.objects.filter(datess__date=now_time, deletes=False).all()
        ##count = Account_record.objects.filter(datess__date=search_date, deletes=False).all()
    # else:
    # search_date = now_time
    count = Account_record.objects.filter(datess__date=now_time, deletes=False).all()
    count_list = []
    for i in count:
        count_row = {}
        last_date = get_nday_list2(2, now_time)
        last_date_end_img = Account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
            'end_money_img')

        if len(last_date_end_img) > 0:
            last_date_end_img = Account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
                'end_money_img').get()
            count_row['last_date_end_img'] = last_date_end_img['end_money_img']
        else:
            count_row['last_date_end_img'] = '前一日无截图'
        print(count_row['last_date_end_img'])
        count_row['id'] = i.id
        count_row['datess'] = i.datess
        count_row['account_name'] = i.account_name
        count_row['start_money'] = i.start_money
        count_row['end_money'] = i.end_money
        count_row['weixin_withdraw_money'] = i.weixin_withdraw_money
        count_row['start_money_img'] = i.start_money_img
        count_row['end_money_img'] = i.end_money_img
        count_row['weixin_img'] = i.weixin_img
        count_row['operator'] = i.operator
        count_row['makes'] = i.makes
        count_list.append(count_row)

    # 财务账户提示账户未确认
    # now_time = time.strftime('%Y-%m-%d', time.localtime())
    all_account_makes = Account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    # now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    account_unmakes = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account_unmakes:
        check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name,
                                                      deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name,
                                                          deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    update_passwd = Updata_passwd()
    if rouse == '财务':
        return render(request, 'countmanagement.html',
                      {'title': title, 'account': account, 'count': count_list, 'nowss': search_date, 'user': user, 'update_passwd': update_passwd,
                       'admin_flog': admin_flog})
    else:
        return render(request, 'countmanagement2.html',
                      {'title': title, 'account': account3, 'count': count_list, 'nowss': search_date, 'formm': forms, 'edit_form': edit_form,
                       'user': user, 'admin_flog': admin_flog, 'total_reminds': total_reminds, 'reminds': reminds, 'unmakes': unmakes,
                       'makes': makes, 'update_passwd': update_passwd})


# 店铺账单
def shop_bill(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '店铺账单'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_shop = Shops.objects.filter(deletes=True).first()
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
    pay_money = '%.2f' % pay_money
    # 财务账户提示账户未确认
    now_time2 = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time2, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'shop_bill.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money, 'user': user,
                   'shop_name': shop_name, 'admin_flog': admin_flog, 'update_passwd': update_passwd})


# 子账户账单
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
    now_time2 = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time2, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    update_passwd = Updata_passwd()
    return render(request, 'account_bill.html',
                  {'title': title, 'now_time': now_time, 'account': accounts, 'tables': tables, 'pay_money': pay_money,
                   'update_passwd': update_passwd,
                   'actual_cost': actual_cost, 'user': user, 'account_name': account_names, 'count_stats': count_stats, 'admin_flog': admin_flog})


# 总账户账单
def total_account_bill(request):
    title = '总账户账单'
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    total_account_all = Total_brank_account.objects.filter(deletes=False).all()
    first_account = total_account_all[0]
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_account_post = ''
    if request.method == 'POST':
        first_account_post = request.POST.get('account_name')
        now_time_post = request.POST.get('check_data')
        if first_account_post and now_time_post:
            first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
            now_time = now_time_post
        elif first_account_post and now_time_post == '':
            first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
        elif first_account_post == '' and now_time_post:
            now_time = now_time_post
    first_accounts = first_account.brank_account_set.filter(deletes=False).values('account_name')
    table_list = []
    for account in first_accounts:
        table = Brush_single_entry.objects.filter(add_time__date=now_time, payment_account__account_name=account['account_name'], deletes=False).all()
        table_list.append(table)
    # 财务账户提示账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time2 = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time2, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'total_account_bill.html',
                  {'title': title, 'user': user, 'table_list': table_list, 'now_time': now_time, 'total_account_all': total_account_all,
                   'account_name': first_account_post, 'admin_flog': admin_flog})


# 总账户核对
def check_total_account(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '总账户核对确认'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    total_account_all = Userinfo.objects.filter(username=user, deletes=False).get().total_brank_account.filter(deletes=False).all()
    errs = ''
    total_account_select = ''
    account_cost = 0.0
    total_cost = 0.0
    if len(total_account_all) != 0:
        for f in total_account_all:
            first_total_account = f.total_account_name
            break
        if request.method == 'POST':
            first_total_account = request.POST.get('search_total_account_name')
            total_account_select = first_total_account
            now_time = request.POST.get('check_date')
        account_all = Brank_account.objects.filter(total_account_name__total_account_name=first_total_account, deletes=False).all()
        tables = []
        for account in account_all:
            tables_queryset = Account_record.objects.filter(datess__date=now_time, account_name=account, deletes=False).all()
            for table in tables_queryset:
                tables.append(table)
                account_cost = float(account_cost)
                account_cost = account_cost + (float(table.start_money) - float(table.end_money))
                if table.makes == 'False':
                    errs = '存在未确认的子账户，总账户无法确认'
                    break
            account_cost = float(account_cost)
            account_cost = '%.2f' % account_cost
        unmake_stats = 0
        total_account_make = Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=first_total_account,
                                                                 deletes=False).all()
        if len(total_account_make) == 0:
            errs = '没有该总账户当天的信息，无法核账'
        else:
            total_account_make = total_account_make.get()
            total_cost = float(total_account_make.start_money) - float(total_account_make.end_money)
            total_cost = '%.2f' % total_cost
            if total_account_make.start_money_img and total_account_make.end_money_img:
                pass
            else:
                errs = '该总账户记录没有截图，无法核账'
            if total_account_make.makes == 'False':
                unmake_stats += 1
        edit_form = Edit_forms()
        if total_cost != account_cost:
            errs = '账目存在问题，请仔细核对'
    else:
        errs = '本账号未绑定总账户'
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    # now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    account_unmakes = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account_unmakes:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                      deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                          deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    update_passwd = Updata_passwd()
    return render(request, 'check_total_account2.html',
                  {'title': title, 'tables': tables, 'total_account_all': total_account_all, 'user': user, 'now_time': now_time, 'err': errs,
                   'unmake_stats': unmake_stats, 'edit_form': edit_form, 'total_cost': total_cost, 'account_cost': account_cost,
                   'total_reminds': total_reminds, 'unmakes': unmakes, 'makes': makes, 'reminds': reminds, 'update_passwd': update_passwd,
                   'total_account_select': total_account_select})


# 总账户确认核对
def make_total_account(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    account = request.GET.get('search_total_account_name')
    now_time = request.GET.get('check_date')
    Total_account_record.objects.filter(datess__date=now_time, account_name__total_account_name=account, deletes=False).update(makes=True)
    operators = Userinfo.objects.get(username=user, deletes=False)
    operation_types = '总账户核对成功'
    after_operations = '{日期：%s，总账户名：%s}' % (now_time, account)
    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
    return HttpResponse(json.dumps('确认成功'))


# 按日期查询总账户记录
def search_total_count(request):
    search_date = request.GET.get('search_date')
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=login)
    title = '总账户记录管理'
    total_account_all = Userinfo.objects.filter(username=user, deletes=False).get().total_brank_account.filter(deletes=False).all()
    account2 = Userinfo.objects.filter(username=user, deletes=False).get().total_brank_account.filter(deletes=False).all()
    forms = Forms()
    edit_form = Edit_forms()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    if search_date:
        count = Total_account_record.objects.filter(datess__date=search_date, deletes=False).all()
    else:
        search_date = get_nday_list2(2, now_time)
        count = Total_account_record.objects.filter(datess__date=search_date, deletes=False).all()
    count_list = []
    for i in count:
        count_row = {}
        last_date = get_nday_list2(2, search_date)
        last_date_end_img = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
            'end_money_img')
        if len(last_date_end_img) > 0:
            last_date_end_img = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
                'end_money_img').get()
            count_row['last_date_end_img'] = last_date_end_img['end_money_img']
        else:
            count_row['last_date_end_img'] = '前一日无截图'
        count_row['id'] = i.id
        count_row['datess'] = i.datess
        count_row['account_name'] = i.account_name
        count_row['start_money'] = i.start_money
        count_row['end_money'] = i.end_money
        count_row['start_money_img'] = i.start_money_img
        count_row['end_money_img'] = i.end_money_img
        count_row['operator'] = i.operator.username
        count_row['makes'] = i.makes
        count_list.append(count_row)
        # 财务账户提示总账户未确认
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    account_unmakes = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account_unmakes:
        check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                      deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__gte=now_time, account_name__account_name=i.account_name,
                                                          deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    update_passwd = Updata_passwd()
    if rouse == '财务':
        return render(request, 'total_countmanagement.html',
                      {'title': title, 'count': count_list, 'nowss': search_date, 'user': user, 'admin_flog': admin_flog,
                       'update_passwd': update_passwd})
    else:
        return render(request, 'total_countmanagement2.html',
                      {'title': title, 'account': account2, 'count': count_list, 'nowss': search_date, 'formm': forms, 'edit_form': edit_form,
                       'user': user, 'total_reminds': total_reminds, 'total_account_all': total_account_all, 'reminds': reminds, 'unmakes': unmakes,
                       'update_passwd': update_passwd, 'makes': makes, 'now_time': search_date})


# 总账单
def all_data(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '总账单'
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    payment_types = '本金'
    if request.method == 'POST':
        now_time = request.POST.get('search_date')
        payment_types = request.POST.get('payment_type')
    if payment_types == '全部':
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, deletes=False).all()
    else:
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, payment_type=payment_types, deletes=False).all()
    payment = 0.0
    for table in tables:
        payment += float(table.payment_amount)
    payment = '%.2f' % payment
    # 财务账户提示账户未确认
    now_time_cheack = time.strftime('%Y-%m-%d', time.localtime())
    now_time2 = get_nday_list2(2, now_time_cheack)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time2, makes=False, deletes=False).all()
    if len(all_account_makes) == 0:
        admin_flog = 1
    else:
        admin_flog = 0
    return render(request, 'all_data.html',
                  {'title': title, 'user': user, 'now_time': now_time, 'payment_type': payment_types, 'tables': tables,
                   'admin_flog': admin_flog, 'pay_money': payment})


# 下载喝酒数据
def download_brush(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    userss = user
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=userss, deletes='False').order_by('add_time')
    operators = request.GET.get('operator')
    shopss = request.GET.get('shopname')
    now_time = request.GET.get('add_time')
    if operators and shopss and now_time:
        if shopss == 'alls' and operators == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, deletes='False').order_by('add_time')
        elif shopss == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=operators, deletes='False').order_by(
                'add_time')
        elif operators == 'alls':
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shopss, deletes='False').order_by('add_time')
        else:
            tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shopss, operator__username=operators,
                                                       deletes='False').order_by('add_time')
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "付款账户", "备注", "操作员"]]
    for i in tables:
        row1 = []
        row1.append(i.add_time)
        row1.append(i.shopname)
        row1.append(i.qq_or_weixin)
        row1.append(i.wang_wang_number)
        row1.append(i.online_order_number)
        row1.append(i.transaction_data)
        row1.append(i.payment_type)
        row1.append(i.payment_amount)
        row1.append(i.payment_account.account_name)
        row1.append(i.remarks)
        row1.append(i.operator.username)
        sheet1.append(row1)
    file_names = str(now_time) + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name='测试', file_name=file_names)


# 下载店铺账单
def down_shop_bill(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_shop = Shops.objects.filter(deletes=True).first()
    if first_shop:
        shop_name = first_shop.shopname
    else:
        shop_name = ''
    now_time2 = request.GET.get('check_data')
    shop_name2 = request.GET.get('shop_name')
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, shopname=shop_name, deletes=False).all()
    if now_time2 and shop_name2:
        tables = Brush_single_entry.objects.filter(add_time__date=now_time2, shopname=shop_name2, deletes=False).all()
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "备注", "操作员"]]
    for i in tables:
        row1 = []
        row1.append(i.add_time)
        row1.append(i.shopname)
        row1.append(i.qq_or_weixin)
        row1.append(i.wang_wang_number)
        row1.append(i.online_order_number)
        row1.append(i.transaction_data)
        row1.append(i.payment_type)
        row1.append(i.payment_amount)
        row1.append(i.remarks)
        row1.append(i.operator.username)
        sheet1.append(row1)
    file_names = str(now_time) + '  ' + shop_name + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=shop_name, file_name=file_names)


# 按月下载店铺账单
def down_shop_bill2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    now_time = datetime.datetime.now().month
    first_shop = Shops.objects.filter(deletes=True).first()
    if first_shop:
        shop_name = first_shop.shopname
    else:
        shop_name = ''
    now_time2 = request.GET.get('check_data')
    shop_name2 = request.GET.get('shop_name')
    tables = Brush_single_entry.objects.filter(add_time__month=now_time, shopname=shop_name, deletes=False).all()
    if now_time2 and shop_name2:
        now_time2 = t_mouth(now_time2)
        now_time = now_time2
        tables = Brush_single_entry.objects.filter(add_time__month=now_time2, shopname=shop_name2, deletes=False).all()
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "备注", "操作员"]]
    for i in tables:
        row1 = []
        row1.append(i.add_time)
        row1.append(i.shopname)
        row1.append(i.qq_or_weixin)
        row1.append(i.wang_wang_number)
        row1.append(i.online_order_number)
        row1.append(i.transaction_data)
        row1.append(i.payment_type)
        row1.append(i.payment_amount)
        row1.append(i.remarks)
        row1.append(i.operator.username)
        sheet1.append(row1)
    file_names = str(now_time) + '月  ' + shop_name2 + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=shop_name2, file_name=file_names)


# 按日下载总账户喝酒数据
def down_total_account_brush(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    total_account_all = Total_brank_account.objects.filter(deletes=False).all()
    first_account = total_account_all[0]
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_account_post = request.GET.get('account_name')
    now_time_post = request.GET.get('check_data')
    if first_account_post and now_time_post:
        first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
        now_time = now_time_post
    elif first_account_post and now_time_post == '':
        first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
    elif first_account_post == '' and now_time_post:
        now_time = now_time_post
    first_accounts = first_account.brank_account_set.filter(deletes=False).values('account_name')
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "收入金额", "付款金额", "账户结余", "付款类型", "付款账户", "备注", "操作员"], ]
    account_start_money = Total_account_record.objects.filter(datess__date=now_time,
                                                              account_name__total_account_name=first_account.total_account_name, deletes=False).all()
    if len(account_start_money) > 0:
        account_start_money = Total_account_record.objects.filter(datess__date=now_time,
                                                                  account_name__total_account_name=first_account.total_account_name,
                                                                  deletes=False).values('start_money').get()
        account_start_money = float(account_start_money['start_money'])
    else:
        account_start_money = 0.0
    sheet1.append(["", "", "", "", "", "", account_start_money, "", account_start_money, "", ""])
    for account in first_accounts:
        table = Brush_single_entry.objects.filter(add_time__date=now_time, payment_account__account_name=account['account_name'], deletes=False).all()
        for i in table:
            row1 = []
            row1.append(i.add_time)
            row1.append(i.shopname)
            row1.append(i.qq_or_weixin)
            row1.append(i.wang_wang_number)
            row1.append(i.online_order_number)
            row1.append(i.transaction_data)
            row1.append('')
            row1.append(i.payment_amount)
            account_last_money = account_start_money - float(i.payment_amount)
            account_start_money = account_last_money
            row1.append(account_last_money)
            row1.append(i.payment_type)
            row1.append(i.payment_account.account_name)
            row1.append(i.remarks)
            row1.append(i.operator.username)
            sheet1.append(row1)
    file_names = str(now_time) + '  ' + first_account_post + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=first_account_post, file_name=file_names)


# 按月下载总账户喝酒数据
def down_total_account_brush2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    total_account_all = Total_brank_account.objects.filter(deletes=False).all()
    first_account = total_account_all[0]
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    first_account_post = request.GET.get('account_name')
    now_time_post = request.GET.get('check_data')
    if first_account_post and now_time_post:
        first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
        now_time = now_time_post
    elif first_account_post and now_time_post == '':
        first_account = Total_brank_account.objects.filter(total_account_name=first_account_post, deletes=False).get()
    elif first_account_post == '' and now_time_post:
        now_time = now_time_post
    first_accounts = first_account.brank_account_set.filter(deletes=False).values('account_name')
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "账户结余", "付款账户", "备注", "操作员"]]
    for account in first_accounts:
        account_start_money = Account_record.objects.filter(datess__date=now_time, account_name__account_name=account['account_name'],
                                                            deletes=False).all()
        if len(account_start_money) > 0:
            account_start_money = Account_record.objects.filter(datess__date=now_time, account_name__account_name=account['account_name'],
                                                                deletes=False).values(
                'start_money').get()
            account_start_money = float(account_start_money['start_money'])
        else:
            account_start_money = 0.0
        table = Brush_single_entry.objects.filter(add_time__date=now_time, payment_account__account_name=account['account_name'], deletes=False).all()
        for i in table:
            row1 = []
            row1.append(i.add_time)
            row1.append(i.shopname)
            row1.append(i.qq_or_weixin)
            row1.append(i.wang_wang_number)
            row1.append(i.online_order_number)
            row1.append(i.transaction_data)
            row1.append(i.payment_type)
            row1.append(i.payment_amount)
            account_last_money = account_start_money - float(i.payment_amount)
            account_start_money = account_last_money
            row1.append(account_last_money)
            row1.append(i.payment_account.account_name)
            row1.append(i.remarks)
            row1.append(i.operator.username)
            sheet1.append(row1)
    file_names = str(now_time) + '  ' + first_account_post + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=first_account_post, file_name=file_names)


# 按日下载总账单
def down_all_data(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time2 = request.GET.get('check_data')
    payment_types = request.GET.get('payment_type')
    if now_time2 and payment_types:
        now_time = now_time2
    if payment_types == '全部':
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, deletes=False).all()
    else:
        tables = Brush_single_entry.objects.filter(add_time__date=now_time, payment_type=payment_types, deletes=False).all()
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "备注", "操作员"]]
    for i in tables:
        row1 = []
        row1.append(i.add_time)
        row1.append(i.shopname)
        row1.append(i.qq_or_weixin)
        row1.append(i.wang_wang_number)
        row1.append(i.online_order_number)
        row1.append(i.transaction_data)
        row1.append(i.payment_type)
        row1.append(i.payment_amount)
        row1.append(i.remarks)
        row1.append(i.operator.username)
        sheet1.append(row1)
    file_names = str(now_time) + '  ' + '的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=now_time, file_name=file_names)


# 按月下载总数据
def down_all_data2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    now_time = datetime.datetime.now().month
    now_time2 = request.GET.get('check_data')
    payment_types = request.GET.get('payment_type')
    if now_time2 and payment_types:
        now_time2 = t_mouth(now_time2)
        now_time = now_time2
    if payment_types == '全部':
        tables = Brush_single_entry.objects.filter(add_time__month=now_time, deletes=False).all()
    else:
        tables = Brush_single_entry.objects.filter(add_time__month=now_time, payment_type=payment_types, deletes=False).all()
    sheet1 = [["喝酒时间", "店铺名", "QQ或微信号", "旺旺号", "线上订单号", "成交日期", "付款类型", "付款金额", "备注", "操作员"]]
    for i in tables:
        row1 = []
        row1.append(i.add_time)
        row1.append(i.shopname)
        row1.append(i.qq_or_weixin)
        row1.append(i.wang_wang_number)
        row1.append(i.online_order_number)
        row1.append(i.transaction_data)
        row1.append(i.payment_type)
        row1.append(i.payment_amount)
        row1.append(i.remarks)
        row1.append(i.operator.username)
        sheet1.append(row1)
    file_names = str(now_time) + '月的喝酒数据'
    return excel.make_response_from_array(sheet1, "xlsx", status=200, sheet_name=now_time, file_name=file_names)


#################测试新功能
from erp.views import Verification


def brushmanagement_2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '喝酒'
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    tables = Brush_single_entry.objects.filter(add_time__date=now_time, operator__username=user, deletes='False')
    len_ = len(tables)
    if len_ > 15:
        tables = tables[:len_ - 16:-1]
    else:
        tables = tables[::-1]
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
            if online_order_numbers != '':
                if len(online_order_numbers) != 18:
                    errs = '线上订单号格式错误'
                else:
                    onlys = Brush_single_entry.objects.filter(online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                                              payment_type=payment_types, deletes=False).all()
                    if len(onlys) > 0:
                        errs = '该订单记录已存在'
        if errs == '':
            add_times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            Brush_single_entry.objects.create(shopname=shopnames, qq_or_weixin=qq_or_weixins, wang_wang_number=wang_wang_numbers,
                                              online_order_number=online_order_numbers, transaction_data=transaction_datas,
                                              payment_type=payment_types, payment_amount=payment_amounts,
                                              payment_account=Brank_account.objects.get(account_name=payment_accounts, deletes=False),
                                              operator=operators, remarks=remarkss, deletes=False, add_time=add_times)
            if Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts, deletes=False):
                Account_record.objects.filter(datess__date=now_time, account_name__account_name=payment_accounts, deletes=False).update(makes=False)
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
    # 验证线上订单号是否存在
    online_unexit_num = 0
    order_unexit_num = 0
    tables_list = []
    verification = Verification()
    for table in tables:
        line = {}
        online_order_numbers = table.online_order_number
        online_stats = verification.order_online(online_order_numbers, now_time)
        if online_stats == 0:
            order_stats = verification.special_order(online_order_numbers, now_time)
            if order_stats == 0:
                pass
            else:
                line['online_stats'] = order_stats
                print(order_stats)
                print(type(order_stats))
                order_unexit_num += order_stats - 1
        else:
            line['online_stats'] = online_stats
            online_unexit_num += online_stats
        line['add_time'] = table.add_time
        line['shopname'] = table.shopname
        line['qq_or_weixin'] = table.qq_or_weixin
        line['wang_wang_number'] = table.wang_wang_number
        line['online_order_number'] = table.online_order_number
        line['transaction_data'] = table.transaction_data
        line['payment_type'] = table.payment_type
        line['payment_amount'] = table.payment_amount
        line['payment_account'] = table.payment_account.account_name
        line['remarks'] = table.remarks
        line['id'] = table.id
        tables_list.append(line)
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
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    return render(request, 'erp_templates/新建文件夹/brush2.html',
                  {'title': title, 'account': account, 'shops': shops, 'now_time': now_time, 'tables': tables_list, 'add_brush_form': add_brush_form,
                   'edit_brush_form': edit_brush_form, 'user': user, 'errs': errs, 'reminds': reminds, 'makes': makes, 'unmakes': unmakes,
                   'total_reminds': total_reminds, })
