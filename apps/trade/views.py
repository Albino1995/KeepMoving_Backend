from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.permissons import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
from .models import ShoppingCart

# Create your views here.



class ShoppingCartViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
    获取购物车详情
    create:
    加入购物车
    delete:
    删除购物记录
    update:
    更新购物车
    partial_update:
    部分更新购物车
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def perform_update(self, serializer):
        existed_nums = ShoppingCart.objects.get(id=serializer.instance.id).nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer
