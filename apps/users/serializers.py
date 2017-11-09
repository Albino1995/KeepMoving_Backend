#!/usr/bin/env python
__author__ = 'Albino'

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta

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
