from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Goods, Banner
from .serializers import GoodsSerializer, BannerSerializer
from .filters import GoodsFilter

# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    # 每页显示条数名称
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    获取商品列表
    read:
    获取指定商品详情
    """
    queryset = Goods.objects.all()
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = GoodsFilter
    # 分页
    pagination_class = GoodsPagination
    # 搜索
    search_fields = ('name', 'goods_sn')
    # 排序
    ordering_fields = ('sold_num', 'price')


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer