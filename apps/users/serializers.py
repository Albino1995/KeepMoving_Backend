#!/usr/bin/env python
__author__ = 'Albino'

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from KeepMoving_Backend.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializers(serializers.Serializer):
    """
    短信验证码序列化
    """
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        """
        验证手机号
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")

        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError("距上次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化
    """
    code = serializers.CharField(label="验证码", write_only=True, required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    # 验证用户名是否唯一
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # 设置style后使密码为密文, 设置write_only序列化返回时不包括该字段
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_code:
            last_record = verify_code[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 验证码过期
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            # 验证码错误
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化
    """
    class Meta:
        model = User
        fields = ('name', 'gender', 'mobile', 'email')
