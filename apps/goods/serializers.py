#!/usr/bin/env python
__author__ = 'Albino'

from rest_framework import serializers

from goods.models import Goods, GoodImage, GoodCS, Banner


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品轮播图序列化
    """
    class Meta:
        model = GoodImage
        fields = ("image",)


class GoodsCSSerializer(serializers.ModelSerializer):
    """
    商品色码序列化
    """
    img = GoodsImageSerializer(many=True)

    class Meta:
        model = GoodCS
        fields = ("id", "goods_size", "goods_color", "goods_num", "img")


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化
    """
    cs = GoodsCSSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    """
    轮播图序列化
    """
    class Meta:
        model = Banner
        fields = "__all__"