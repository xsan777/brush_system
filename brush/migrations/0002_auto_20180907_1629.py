# Generated by Django 2.1.1 on 2018-09-07 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brush', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_brank',
            name='brank_operator',
        ),
        migrations.RemoveField(
            model_name='user_brank',
            name='users',
        ),
        migrations.RemoveField(
            model_name='user_shops',
            name='user_shop',
        ),
        migrations.RemoveField(
            model_name='user_shops',
            name='users',
        ),
        migrations.DeleteModel(
            name='User_Brank',
        ),
        migrations.DeleteModel(
            name='User_Shops',
        ),
        migrations.DeleteModel(
            name='Userinfo',
        ),
    ]
