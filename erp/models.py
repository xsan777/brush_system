# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ErpTaskLog(models.Model):
    datetime = models.DateTimeField(primary_key=True)
    mode = models.CharField(max_length=30)
    parameter = models.CharField(max_length=255, blank=True, null=True)
    sql = models.CharField(max_length=20, blank=True, null=True)
    db = models.CharField(max_length=20, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ERP_task_log'
        unique_together = (('datetime', 'mode'),)


class InventoryQuery(models.Model):
    defective_qty = models.IntegerField(blank=True, null=True)
    i_id = models.CharField(max_length=10, blank=True, null=True)
    in_qty = models.IntegerField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    order_lock = models.IntegerField(blank=True, null=True)
    purchase_qty = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    return_qty = models.IntegerField(blank=True, null=True)
    sku_id = models.CharField(primary_key=True, max_length=30)
    virtual_qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory.query'


class JstOrdersOutQuery(models.Model):
    co_id = models.CharField(max_length=10, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    io_id = models.CharField(primary_key=True, max_length=10)
    is_cod = models.CharField(max_length=6, blank=True, null=True)
    lc_id = models.CharField(max_length=12, blank=True, null=True)
    logistics_company = models.CharField(max_length=12, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)
    pay_amount = models.FloatField(blank=True, null=True)
    receiver_address = models.CharField(max_length=100, blank=True, null=True)
    receiver_city = models.CharField(max_length=20, blank=True, null=True)
    receiver_district = models.CharField(max_length=50, blank=True, null=True)
    receiver_mobile = models.CharField(max_length=15, blank=True, null=True)
    receiver_name = models.CharField(max_length=30, blank=True, null=True)
    receiver_state = models.CharField(max_length=15, blank=True, null=True)
    shop_buyer_id = models.CharField(max_length=25, blank=True, null=True)
    shop_id = models.CharField(max_length=8, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    remark = models.CharField(max_length=350, blank=True, null=True)
    buyer_message = models.CharField(max_length=80, blank=True, null=True)
    receiver_phone = models.CharField(max_length=20, blank=True, null=True)
    invoice_title = models.CharField(max_length=20, blank=True, null=True)
    receiver_country = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.out.query'


class JstOrdersOutQueryItems(models.Model):
    ioi_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=80, blank=True, null=True)
    pic = models.CharField(max_length=150, blank=True, null=True)
    properties_value = models.CharField(max_length=40, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    sale_amount = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    sku_id = models.CharField(max_length=30, blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.out.query.items'


class JstOrdersQuery(models.Model):
    co_id = models.CharField(max_length=10, blank=True, null=True)
    free_amount = models.IntegerField(blank=True, null=True)
    freight = models.FloatField(blank=True, null=True)
    invoice_title = models.CharField(max_length=20, blank=True, null=True)
    is_cod = models.CharField(max_length=6, blank=True, null=True)
    items = models.IntegerField(blank=True, null=True)
    l_id = models.CharField(max_length=20, blank=True, null=True)
    lc_id = models.CharField(max_length=12, blank=True, null=True)
    logistics_company = models.CharField(max_length=12, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    o_id = models.CharField(primary_key=True, max_length=10)
    order_date = models.DateTimeField(blank=True, null=True)
    order_from = models.CharField(max_length=20, blank=True, null=True)
    outer_pay_id = models.CharField(max_length=40, blank=True, null=True)
    pay_amount = models.FloatField(blank=True, null=True)
    pay_date = models.DateTimeField(blank=True, null=True)
    question_desc = models.CharField(max_length=30, blank=True, null=True)
    question_type = models.CharField(max_length=10, blank=True, null=True)
    receiver_address = models.CharField(max_length=100, blank=True, null=True)
    receiver_city = models.CharField(max_length=20, blank=True, null=True)
    receiver_district = models.CharField(max_length=50, blank=True, null=True)
    receiver_mobile = models.CharField(max_length=15, blank=True, null=True)
    receiver_name = models.CharField(max_length=30, blank=True, null=True)
    receiver_state = models.CharField(max_length=15, blank=True, null=True)
    remark = models.CharField(max_length=350, blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    shop_buyer_id = models.CharField(max_length=25, blank=True, null=True)
    shop_id = models.CharField(max_length=8, blank=True, null=True)
    shop_name = models.CharField(max_length=10, blank=True, null=True)
    shop_status = models.CharField(max_length=30, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(max_length=4, blank=True, null=True)
    wms_co_id = models.CharField(max_length=8, blank=True, null=True)
    buyer_message = models.CharField(max_length=80, blank=True, null=True)
    receiver_phone = models.CharField(max_length=20, blank=True, null=True)
    tag = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.query'


class JstOrdersQueryItems(models.Model):
    amount = models.FloatField(blank=True, null=True)
    base_price = models.FloatField(blank=True, null=True)
    i_id = models.CharField(max_length=10, blank=True, null=True)
    is_gift = models.CharField(max_length=6, blank=True, null=True)
    item_status = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    oi_id = models.CharField(primary_key=True, max_length=11)
    outer_oi_id = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    properties_value = models.CharField(max_length=40, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    raw_so_id = models.CharField(max_length=20, blank=True, null=True)
    refund_id = models.CharField(max_length=20, blank=True, null=True)
    refund_status = models.CharField(max_length=10, blank=True, null=True)
    shop_sku_id = models.CharField(max_length=20, blank=True, null=True)
    sku_id = models.CharField(max_length=30, blank=True, null=True)
    refund_qty = models.IntegerField(blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.query.items'


class JstOrdersQueryPays(models.Model):
    amount = models.FloatField(blank=True, null=True)
    buyer_account = models.CharField(max_length=40, blank=True, null=True)
    is_order_pay = models.CharField(max_length=6, blank=True, null=True)
    outer_pay_id = models.CharField(max_length=40, blank=True, null=True)
    pay_date = models.DateTimeField(blank=True, null=True)
    pay_id = models.CharField(primary_key=True, max_length=8)
    payment = models.CharField(max_length=10, blank=True, null=True)
    seller_account = models.CharField(max_length=40, blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.query.pays'


class JstOrdersQuerySpecialSingle(models.Model):
    o_id = models.IntegerField(primary_key=True)
    create_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    pay_amount = models.FloatField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    pay_date = models.DateTimeField(blank=True, null=True)
    question_type = models.CharField(max_length=100, blank=True, null=True)
    question_desc = models.CharField(max_length=100, blank=True, null=True)
    shop_name = models.CharField(max_length=10, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    shop_buyer_id = models.CharField(max_length=25, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.orders.query.special_single'


class JstRefundQuery(models.Model):
    as_date = models.DateTimeField(blank=True, null=True)
    as_id = models.CharField(primary_key=True, max_length=10)
    good_status = models.CharField(max_length=20, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)
    outer_as_id = models.CharField(max_length=20, blank=True, null=True)
    payment = models.FloatField(blank=True, null=True)
    question_type = models.CharField(max_length=10, blank=True, null=True)
    receiver_name = models.CharField(max_length=30, blank=True, null=True)
    refund = models.FloatField(blank=True, null=True)
    shop_buyer_id = models.CharField(max_length=25, blank=True, null=True)
    shop_id = models.CharField(max_length=8, blank=True, null=True)
    shop_name = models.CharField(max_length=10, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(max_length=4, blank=True, null=True)
    warehouse = models.CharField(max_length=30, blank=True, null=True)
    l_id = models.CharField(max_length=20, blank=True, null=True)
    logistics_company = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.refund.query'


class JstRefundQueryItems(models.Model):
    asi_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=255, blank=True, null=True)
    pic = models.CharField(max_length=150, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    properties_value = models.CharField(max_length=40, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    r_qty = models.IntegerField(blank=True, null=True)
    sku_id = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=4, blank=True, null=True)
    o_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jst.refund.query.items'


class LogisticQuery(models.Model):
    l_id = models.CharField(max_length=16, blank=True, null=True)
    lc_id = models.CharField(max_length=12, blank=True, null=True)
    logistics_company = models.CharField(max_length=12, blank=True, null=True)
    o_id = models.CharField(primary_key=True, max_length=10)
    send_date = models.DateTimeField(blank=True, null=True)
    shop_id = models.CharField(max_length=8, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    freight = models.CharField(max_length=8, blank=True, null=True)
    weight = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logistic.query'


class LogisticQueryItems(models.Model):
    o_id = models.CharField(max_length=10, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    raw_so_id = models.CharField(primary_key=True, max_length=20)
    sku_id = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logistic.query.items'


class PurchaseQuery(models.Model):
    item_type = models.CharField(max_length=10, blank=True, null=True)
    po_date = models.DateTimeField(blank=True, null=True)
    po_id = models.CharField(primary_key=True, max_length=10)
    purchaser_name = models.CharField(max_length=10, blank=True, null=True)
    remark = models.CharField(max_length=350, blank=True, null=True)
    seller = models.CharField(max_length=10, blank=True, null=True)
    send_address = models.CharField(max_length=100, blank=True, null=True)
    so_id = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    supplier_id = models.CharField(max_length=10, blank=True, null=True)
    tax_rate = models.CharField(max_length=10, blank=True, null=True)
    term = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase.query'


class PurchaseQueryItems(models.Model):
    i_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    po_id = models.CharField(max_length=10, blank=True, null=True)
    poi_id = models.CharField(primary_key=True, max_length=10)
    price = models.FloatField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    sku_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase.query.items'


class PurchaseinQuery(models.Model):
    io_date = models.DateTimeField(blank=True, null=True)
    io_id = models.CharField(max_length=10, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    po_id = models.CharField(max_length=10, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    supplier_id = models.CharField(max_length=10, blank=True, null=True)
    supplier_name = models.CharField(max_length=30, blank=True, null=True)
    warehouse = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchasein.query'


class PurchaseinQueryItems(models.Model):
    cost_amount = models.FloatField(blank=True, null=True)
    cost_price = models.CharField(max_length=12, blank=True, null=True)
    io_id = models.CharField(max_length=10, blank=True, null=True)
    ioi_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=80, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    sku_id = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchasein.query.items'


class PurchaseoutQuery(models.Model):
    io_id = models.CharField(primary_key=True, max_length=10)
    io_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    so_id = models.CharField(max_length=18, blank=True, null=True)
    f_status = models.CharField(max_length=20, blank=True, null=True)
    warehouse = models.CharField(max_length=30, blank=True, null=True)
    receiver_name = models.CharField(max_length=30, blank=True, null=True)
    receiver_mobile = models.CharField(max_length=15, blank=True, null=True)
    receiver_state = models.CharField(max_length=15, blank=True, null=True)
    receiver_city = models.CharField(max_length=20, blank=True, null=True)
    receiver_district = models.CharField(max_length=50, blank=True, null=True)
    receiver_address = models.CharField(max_length=100, blank=True, null=True)
    wh_id = models.CharField(max_length=5, blank=True, null=True)
    remark = models.CharField(max_length=350, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    po_id = models.CharField(max_length=10, blank=True, null=True)
    wms_co_id = models.CharField(max_length=8, blank=True, null=True)
    seller_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchaseout.query'


class PurchaseoutQueryItems(models.Model):
    ioi_id = models.CharField(primary_key=True, max_length=10)
    sku_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    properties_value = models.CharField(max_length=10, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    cost_price = models.FloatField(blank=True, null=True)
    cost_amount = models.FloatField(blank=True, null=True)
    i_id = models.CharField(max_length=10, blank=True, null=True)
    remark = models.CharField(max_length=60, blank=True, null=True)
    io_id = models.CharField(max_length=10, blank=True, null=True)
    co_id = models.CharField(max_length=10, blank=True, null=True)
    invoice_title = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchaseout.query.items'


class ShopsQuery(models.Model):
    created = models.DateTimeField(blank=True, null=True)
    nick = models.CharField(max_length=20, blank=True, null=True)
    session_expired = models.DateTimeField(blank=True, null=True)
    shop_id = models.CharField(primary_key=True, max_length=8)
    shop_name = models.CharField(max_length=10, blank=True, null=True)
    shop_site = models.CharField(max_length=10, blank=True, null=True)
    shop_url = models.CharField(max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    operator = models.CharField(max_length=20, blank=True, null=True)
    brand = models.CharField(max_length=20, blank=True, null=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    sn = models.CharField(db_column='SN', unique=True, max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shops.query'


class ShopsQueryCopy(models.Model):
    created = models.DateTimeField(blank=True, null=True)
    nick = models.CharField(max_length=20, blank=True, null=True)
    session_expired = models.DateTimeField(blank=True, null=True)
    shop_id = models.CharField(primary_key=True, max_length=8)
    shop_name = models.CharField(max_length=10, blank=True, null=True)
    shop_site = models.CharField(max_length=10, blank=True, null=True)
    shop_url = models.CharField(max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    operator = models.CharField(max_length=20, blank=True, null=True)
    brand = models.CharField(max_length=20, blank=True, null=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    sn = models.CharField(db_column='SN', unique=True, max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shops.query_copy'


class SkuQuery(models.Model):
    brand = models.CharField(max_length=10, blank=True, null=True)
    c_id = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    cost_price = models.CharField(max_length=12, blank=True, null=True)
    enabled = models.IntegerField(blank=True, null=True)
    i_id = models.CharField(max_length=10, blank=True, null=True)
    market_price = models.CharField(max_length=12, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    pic = models.CharField(max_length=150, blank=True, null=True)
    pic_big = models.CharField(max_length=150, blank=True, null=True)
    properties_name = models.CharField(max_length=40, blank=True, null=True)
    properties_value = models.CharField(max_length=40, blank=True, null=True)
    sale_price = models.CharField(max_length=12, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    sku_code = models.CharField(max_length=20, blank=True, null=True)
    sku_id = models.CharField(primary_key=True, max_length=30)
    sku_type = models.CharField(max_length=10, blank=True, null=True)
    supplier_i_id = models.CharField(max_length=10, blank=True, null=True)
    supplier_id = models.CharField(max_length=10, blank=True, null=True)
    supplier_name = models.CharField(max_length=30, blank=True, null=True)
    supplier_sku_id = models.CharField(max_length=10, blank=True, null=True)
    vc_name = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sku.query'
