from rest_framework import mixins, viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.permissons import IsOwnerOrReadOnly
from .serializers import UserFavDetailSerializer, UserFavSerializer, LeavingMessageSerializer, AddressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
    新建收藏
    list:
    获取用户收藏
    read:
    根据商品查询当前用户收藏信息
    delete:
    根据商品删除当前用户收藏信息
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
    获取用户留言
    create:
    添加留言
    delete:
    删除留言
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 重载GenericAPIView中的get_queryset获取当前用户的留言
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    list:
    获取收货地址
    create:
    新增收货地址
    delete:
    删除收货地址
    update:
    更新收货地址
    partial_update:
    部分更新收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
