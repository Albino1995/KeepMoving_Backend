from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.permissons import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderDetailSerializer, OrderSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

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


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
    显示个人全部订单
    create:
    创建订单
    delete:
    取消订单
    read:
    单条订单详细记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shopping_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shopping_cart in shopping_carts:
            order_goods = OrderGoods()
            order_goods.goods = shopping_cart.goods
            order_goods.goods_num = shopping_cart.nums
            order_goods.order = order
            order_goods.save()
            # 删除购物车记录
            shopping_cart.delete()
        return order
