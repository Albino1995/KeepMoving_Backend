#!/usr/bin/env python
__author__ = 'Albino'

import django_filters

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    price_min = django_filters.NumberFilter(name='price', lookup_expr='gte', help_text='最低价')
    price_max = django_filters.NumberFilter(name='price', lookup_expr='lte', help_text='最高价')
    gender = django_filters.ChoiceFilter(name='gender', choices=(("male", "男的"), ("female", "女的"), ("neutral", "男女同款")),
                                         help_text='性别')
    category = django_filters.ChoiceFilter(name='category', choices=(("踩的", "踩的"), ("穿的", "穿的"), ("戴的", "戴的")),
                                           help_text='类别')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot', 'is_new', 'is_sale']
