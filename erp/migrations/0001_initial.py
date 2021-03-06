# Generated by Django 2.1.1 on 2018-09-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErpTaskLog',
            fields=[
                ('datetime', models.DateTimeField(primary_key=True, serialize=False)),
                ('mode', models.CharField(max_length=30)),
                ('parameter', models.CharField(blank=True, max_length=255, null=True)),
                ('sql', models.CharField(blank=True, max_length=20, null=True)),
                ('db', models.CharField(blank=True, max_length=20, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ERP_task_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryQuery',
            fields=[
                ('defective_qty', models.IntegerField(blank=True, null=True)),
                ('i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('in_qty', models.IntegerField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('order_lock', models.IntegerField(blank=True, null=True)),
                ('purchase_qty', models.IntegerField(blank=True, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('return_qty', models.IntegerField(blank=True, null=True)),
                ('sku_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('virtual_qty', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'inventory.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersOutQuery',
            fields=[
                ('co_id', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('io_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('is_cod', models.CharField(blank=True, max_length=6, null=True)),
                ('lc_id', models.CharField(blank=True, max_length=12, null=True)),
                ('logistics_company', models.CharField(blank=True, max_length=12, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
                ('pay_amount', models.FloatField(blank=True, null=True)),
                ('receiver_address', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_city', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_district', models.CharField(blank=True, max_length=50, null=True)),
                ('receiver_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=30, null=True)),
                ('receiver_state', models.CharField(blank=True, max_length=15, null=True)),
                ('shop_buyer_id', models.CharField(blank=True, max_length=25, null=True)),
                ('shop_id', models.CharField(blank=True, max_length=8, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('remark', models.CharField(blank=True, max_length=350, null=True)),
                ('buyer_message', models.CharField(blank=True, max_length=80, null=True)),
                ('receiver_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('invoice_title', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_country', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.orders.out.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersOutQueryItems',
            fields=[
                ('ioi_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('pic', models.CharField(blank=True, max_length=150, null=True)),
                ('properties_value', models.CharField(blank=True, max_length=40, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('sale_amount', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=30, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.orders.out.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersQuery',
            fields=[
                ('co_id', models.CharField(blank=True, max_length=10, null=True)),
                ('free_amount', models.IntegerField(blank=True, null=True)),
                ('freight', models.FloatField(blank=True, null=True)),
                ('invoice_title', models.CharField(blank=True, max_length=20, null=True)),
                ('is_cod', models.CharField(blank=True, max_length=6, null=True)),
                ('items', models.IntegerField(blank=True, null=True)),
                ('l_id', models.CharField(blank=True, max_length=20, null=True)),
                ('lc_id', models.CharField(blank=True, max_length=12, null=True)),
                ('logistics_company', models.CharField(blank=True, max_length=12, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('o_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('order_from', models.CharField(blank=True, max_length=20, null=True)),
                ('outer_pay_id', models.CharField(blank=True, max_length=40, null=True)),
                ('pay_amount', models.FloatField(blank=True, null=True)),
                ('pay_date', models.DateTimeField(blank=True, null=True)),
                ('question_desc', models.CharField(blank=True, max_length=30, null=True)),
                ('question_type', models.CharField(blank=True, max_length=10, null=True)),
                ('receiver_address', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_city', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_district', models.CharField(blank=True, max_length=50, null=True)),
                ('receiver_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=30, null=True)),
                ('receiver_state', models.CharField(blank=True, max_length=15, null=True)),
                ('remark', models.CharField(blank=True, max_length=350, null=True)),
                ('send_date', models.DateTimeField(blank=True, null=True)),
                ('shop_buyer_id', models.CharField(blank=True, max_length=25, null=True)),
                ('shop_id', models.CharField(blank=True, max_length=8, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=10, null=True)),
                ('shop_status', models.CharField(blank=True, max_length=30, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('type', models.CharField(blank=True, max_length=4, null=True)),
                ('wms_co_id', models.CharField(blank=True, max_length=8, null=True)),
                ('buyer_message', models.CharField(blank=True, max_length=80, null=True)),
                ('receiver_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('tag', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'jst.orders.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersQueryItems',
            fields=[
                ('amount', models.FloatField(blank=True, null=True)),
                ('base_price', models.FloatField(blank=True, null=True)),
                ('i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('is_gift', models.CharField(blank=True, max_length=6, null=True)),
                ('item_status', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('oi_id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('outer_oi_id', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('properties_value', models.CharField(blank=True, max_length=40, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('raw_so_id', models.CharField(blank=True, max_length=20, null=True)),
                ('refund_id', models.CharField(blank=True, max_length=20, null=True)),
                ('refund_status', models.CharField(blank=True, max_length=10, null=True)),
                ('shop_sku_id', models.CharField(blank=True, max_length=20, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=30, null=True)),
                ('refund_qty', models.IntegerField(blank=True, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.orders.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersQueryPays',
            fields=[
                ('amount', models.FloatField(blank=True, null=True)),
                ('buyer_account', models.CharField(blank=True, max_length=40, null=True)),
                ('is_order_pay', models.CharField(blank=True, max_length=6, null=True)),
                ('outer_pay_id', models.CharField(blank=True, max_length=40, null=True)),
                ('pay_date', models.DateTimeField(blank=True, null=True)),
                ('pay_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('payment', models.CharField(blank=True, max_length=10, null=True)),
                ('seller_account', models.CharField(blank=True, max_length=40, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.orders.query.pays',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstOrdersQuerySpecialSingle',
            fields=[
                ('o_id', models.IntegerField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('pay_amount', models.FloatField(blank=True, null=True)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('pay_date', models.DateTimeField(blank=True, null=True)),
                ('question_type', models.CharField(blank=True, max_length=100, null=True)),
                ('question_desc', models.CharField(blank=True, max_length=100, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.orders.query.special_single',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstRefundQuery',
            fields=[
                ('as_date', models.DateTimeField(blank=True, null=True)),
                ('as_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('good_status', models.CharField(blank=True, max_length=20, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
                ('outer_as_id', models.CharField(blank=True, max_length=20, null=True)),
                ('payment', models.FloatField(blank=True, null=True)),
                ('question_type', models.CharField(blank=True, max_length=10, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=30, null=True)),
                ('refund', models.FloatField(blank=True, null=True)),
                ('shop_buyer_id', models.CharField(blank=True, max_length=25, null=True)),
                ('shop_id', models.CharField(blank=True, max_length=8, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=10, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('type', models.CharField(blank=True, max_length=4, null=True)),
                ('warehouse', models.CharField(blank=True, max_length=30, null=True)),
                ('l_id', models.CharField(blank=True, max_length=20, null=True)),
                ('logistics_company', models.CharField(blank=True, max_length=12, null=True)),
            ],
            options={
                'db_table': 'jst.refund.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JstRefundQueryItems',
            fields=[
                ('asi_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('pic', models.CharField(blank=True, max_length=150, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('properties_value', models.CharField(blank=True, max_length=40, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('r_qty', models.IntegerField(blank=True, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, max_length=4, null=True)),
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'jst.refund.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LogisticQuery',
            fields=[
                ('l_id', models.CharField(blank=True, max_length=16, null=True)),
                ('lc_id', models.CharField(blank=True, max_length=12, null=True)),
                ('logistics_company', models.CharField(blank=True, max_length=12, null=True)),
                ('o_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('send_date', models.DateTimeField(blank=True, null=True)),
                ('shop_id', models.CharField(blank=True, max_length=8, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
            ],
            options={
                'db_table': 'logistic.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LogisticQueryItems',
            fields=[
                ('o_id', models.CharField(blank=True, max_length=10, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('raw_so_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('sku_id', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'logistic.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseinQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('io_date', models.DateTimeField(blank=True, null=True)),
                ('io_id', models.CharField(blank=True, max_length=10, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('po_id', models.CharField(blank=True, max_length=10, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('supplier_id', models.CharField(blank=True, max_length=10, null=True)),
                ('supplier_name', models.CharField(blank=True, max_length=30, null=True)),
                ('warehouse', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'purchasein.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseinQueryItems',
            fields=[
                ('cost_amount', models.FloatField(blank=True, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('io_id', models.CharField(blank=True, max_length=10, null=True)),
                ('ioi_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'purchasein.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseoutQuery',
            fields=[
                ('io_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('io_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('so_id', models.CharField(blank=True, max_length=18, null=True)),
                ('f_status', models.CharField(blank=True, max_length=20, null=True)),
                ('warehouse', models.CharField(blank=True, max_length=30, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=30, null=True)),
                ('receiver_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_state', models.CharField(blank=True, max_length=15, null=True)),
                ('receiver_city', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_district', models.CharField(blank=True, max_length=50, null=True)),
                ('receiver_address', models.CharField(blank=True, max_length=100, null=True)),
                ('wh_id', models.CharField(blank=True, max_length=5, null=True)),
                ('remark', models.CharField(blank=True, max_length=350, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('po_id', models.CharField(blank=True, max_length=10, null=True)),
                ('wms_co_id', models.CharField(blank=True, max_length=8, null=True)),
                ('seller_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'purchaseout.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseoutQueryItems',
            fields=[
                ('ioi_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('sku_id', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('properties_value', models.CharField(blank=True, max_length=10, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('cost_amount', models.FloatField(blank=True, null=True)),
                ('i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=60, null=True)),
                ('io_id', models.CharField(blank=True, max_length=10, null=True)),
                ('co_id', models.CharField(blank=True, max_length=10, null=True)),
                ('invoice_title', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'purchaseout.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseQuery',
            fields=[
                ('item_type', models.CharField(blank=True, max_length=10, null=True)),
                ('po_date', models.DateTimeField(blank=True, null=True)),
                ('po_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('purchaser_name', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=350, null=True)),
                ('seller', models.CharField(blank=True, max_length=10, null=True)),
                ('send_address', models.CharField(blank=True, max_length=100, null=True)),
                ('so_id', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, max_length=16, null=True)),
                ('supplier_id', models.CharField(blank=True, max_length=10, null=True)),
                ('tax_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('term', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'purchase.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseQueryItems',
            fields=[
                ('i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('po_id', models.CharField(blank=True, max_length=10, null=True)),
                ('poi_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('price', models.FloatField(blank=True, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'purchase.query.items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShopsQuery',
            fields=[
                ('created', models.DateTimeField(blank=True, null=True)),
                ('nick', models.CharField(blank=True, max_length=20, null=True)),
                ('session_expired', models.DateTimeField(blank=True, null=True)),
                ('shop_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('shop_name', models.CharField(blank=True, max_length=10, null=True)),
                ('shop_site', models.CharField(blank=True, max_length=10, null=True)),
                ('shop_url', models.CharField(blank=True, max_length=50, null=True)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
                ('operator', models.CharField(blank=True, max_length=20, null=True)),
                ('brand', models.CharField(blank=True, max_length=20, null=True)),
                ('abbreviation', models.CharField(blank=True, max_length=10, null=True)),
                ('sn', models.CharField(blank=True, db_column='SN', max_length=2, null=True, unique=True)),
            ],
            options={
                'db_table': 'shops.query',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SkuQuery',
            fields=[
                ('brand', models.CharField(blank=True, max_length=10, null=True)),
                ('c_id', models.CharField(blank=True, max_length=10, null=True)),
                ('category', models.CharField(blank=True, max_length=10, null=True)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('enabled', models.IntegerField(blank=True, null=True)),
                ('i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('market_price', models.FloatField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('pic', models.CharField(blank=True, max_length=150, null=True)),
                ('pic_big', models.CharField(blank=True, max_length=150, null=True)),
                ('properties_name', models.CharField(blank=True, max_length=40, null=True)),
                ('properties_value', models.CharField(blank=True, max_length=40, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
                ('sku_code', models.CharField(blank=True, max_length=20, null=True)),
                ('sku_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('sku_type', models.CharField(blank=True, max_length=10, null=True)),
                ('supplier_i_id', models.CharField(blank=True, max_length=10, null=True)),
                ('supplier_id', models.CharField(blank=True, max_length=10, null=True)),
                ('supplier_name', models.CharField(blank=True, max_length=30, null=True)),
                ('supplier_sku_id', models.CharField(blank=True, max_length=10, null=True)),
                ('vc_name', models.CharField(blank=True, max_length=20, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sku.query',
                'managed': False,
            },
        ),
    ]
