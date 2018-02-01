from datetime import datetime
from django.shortcuts import redirect
from rest_framework import mixins, viewsets, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.alipay import AliPay

from utils.permissons import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderDetailSerializer, OrderSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import GoodCS
from KeepMoving_Backend.settings import private_key_path, ali_pub_key_path

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
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('add_time',)

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


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid="2016080900200120",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            # 订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝交易号
            trade_no = processed_dict.get('trade_no', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods.goods
                    goods.sold_num += order_good.goods_num
                    goods_cs = order_good.goods
                    goods_cs.goods_num -= order_good.goods_num
                    goods_cs.save()
                    goods.save()
                existed_order.pay_status = "TRADE_SUCCESS"
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("http://127.0.0.1:8000/index#/success")
            return response
        else:
            response = redirect("http://127.0.0.1:8000/index#/success")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url返回
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid="2016080900200120",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            # 订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝交易号
            trade_no = processed_dict.get('trade_no', None)
            # 支付宝订单状态
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")