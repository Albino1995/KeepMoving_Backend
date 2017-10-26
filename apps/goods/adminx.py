import xadmin
from .models import Goods, GoodCS, GoodImage, Banner


class GoodsAdmin():
    list_display = ['category', 'goods_sn', 'name', 'sold_num', 'fav_num', 'price', 'gender', 'goods_desc', 'is_new',
                    'is_hot', 'is_sale', 'add_time']
    search_fields = ['name', ]
    list_editable = ["is_hot", "is_new", "is_sale"]
    list_filter = ['category', 'goods_sn', 'name', 'sold_num', 'fav_num', 'price', 'gender', 'goods_desc', 'is_new',
                   'is_hot', 'is_sale', 'add_time']
    style_fields = {"goods_desc": "ueditor"}


class GoodCSAdmin():
    list_display = ["goods", "goods_size", "goods_color", "goods_num", "add_time"]
    search_fields = ['goods__name', ]
    list_filter = ["goods", "goods_size", "goods_color", "goods_num", "add_time"]

    class GoodImageInline():
        model = GoodImage
        exclude = ["add_time"]
        # 起始数量
        extra = 1
        style = 'tab'

    inlines = [GoodImageInline]


class BannerAdmin(object):
    list_display = ["image", "index"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodCS, GoodCSAdmin)
xadmin.site.register(Banner, BannerAdmin)
