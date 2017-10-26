import xadmin
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin():
    list_display = ["user", "goods", "nums"]


class OrderInfoAdmin():
    list_display = ["user", "order_sn", "trade_no", "pay_status", "order_mount", "pay_time", "add_time"]

    class OrderGoodsInline():
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
