#!/usr/bin/env python
__author__ = 'Albino'

import time
import random
import string
import re
from rest_framework import serializers

from utils.alipay import AliPay
from KeepMoving_Backend.settings import REGEX_MOBILE, private_key_path, ali_pub_key_path
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import GoodCS
from goods.serializers import GoodsCSSerializer


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车记录序列化，一个购物车只有一条单个的商品记录
    """
    goods = GoodsCSSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化，使用Serializer防止添加相同商品到购物车报错
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 外键字段，使用Serializer带上queryset
    goods = serializers.PrimaryKeyRelatedField(required=True, label='商品名称', queryset=GoodCS.objects.all())
    nums = serializers.IntegerField(required=True, label='数量', min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能少于1",
                                        "required": "请填写购买数量"
                                    })

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        if nums > goods.goods_num:
            raise serializers.ValidationError({"nums": ["商品数量不能大于库存"]})
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 针对从商品页增加购物车数量
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        """
        针对在购物车修改数量
        """
        instance.nums = validated_data["nums"]
        if instance.nums > instance.goods.goods_num:
            raise serializers.ValidationError({"nums": ["商品数量不能大于库存"]})
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    一条商品订单记录序列化
    """
    goods = GoodsCSSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单详情序列化
    """
    goods = OrderGoodsSerializer(many=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016080900200120",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    订单序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    order_mount = serializers.FloatField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号 当前时间 + userid + 随机数
        order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                         user_id=self.context["request"].user.id,
                                                         ran_str="".join(
                                                             random.choice(string.digits) for x in range(2)))
        return order_sn

    def validate(self, attrs):
        shopping_carts = ShoppingCart.objects.filter(user=self.context['request'].user)
        total_price = 0
        for shopping_cart in shopping_carts:
            total_price += shopping_cart.goods.goods.price * shopping_cart.nums
        attrs["order_mount"] = total_price
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    def validate_signer_mobile(self, signer_mobile):
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码不合法")

        return signer_mobile

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016080900200120",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = ("user", "order_sn", "trade_no", "pay_status", "order_mount", "pay_time", "address", "signer_name",
                  "signer_mobile", "add_time", "alipay_url")
