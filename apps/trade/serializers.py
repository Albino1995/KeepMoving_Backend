#!/usr/bin/env python
__author__ = 'Albino'

from rest_framework import serializers

from .models import ShoppingCart
from goods.models import GoodCS
from goods.serializers import GoodsCSSerializer


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车记录序列化
    """
    goods = GoodsCSSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
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
            raise serializers.ValidationError("商品数量不能大于库存")
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
            raise serializers.ValidationError("商品数量不能大于库存")
        instance.save()
        return instance
