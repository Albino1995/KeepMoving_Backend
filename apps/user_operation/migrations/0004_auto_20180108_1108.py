# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-08 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20171109_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品型号id', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
    ]
