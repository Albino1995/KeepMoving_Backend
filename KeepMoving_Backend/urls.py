"""KeepMoving_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, BannerViewSet
from users.views import SmsCodeViewSet
from KeepMoving_Backend.settings import MEDIA_ROOT

router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")
# 配置banners的url
router.register(r'banners', BannerViewSet, base_name="banners")
# 配置codes的url,用于验证码
router.register(r'codes', SmsCodeViewSet, base_name="codes")

urlpatterns = [
    # xadmin
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    # 文档
    url(r'docs/', include_docs_urls(title="KeepMoving")),
    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),
]
