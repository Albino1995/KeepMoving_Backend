#!/usr/bin/env python
__author__ = 'Albino'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsCSSerializer
from .models import UserFav, UserLeavingMessage


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsCSSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")

class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已收藏"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 设置read_only, 只返回不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")