import string
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import SmsSerializers
from utils.yunpian import YunPian
from KeepMoving_Backend.settings import API_KEY
from .models import VerifyCode

# Create your views here.

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    发送手机验证码
    """
    serializer_class = SmsSerializers

    def generate_code(self):
        """
        生成四位数字验证码
        """
        ALL_LETTER = string.digits
        return "".join(random.choice(ALL_LETTER) for i in range(4))

    def create(self, request, *args, **kwargs):
        """
        重写create方法
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        yunpian = YunPian(API_KEY)
        code = self.generate_code()
        sms_status = yunpian.send_sms(code, mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存记录到数据库
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

