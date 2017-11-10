#!/usr/bin/env python
__author__ = 'Albino'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from trade.models import ShoppingCart


# 完成后在apps中设置ready函数
@receiver(post_save, sender=ShoppingCart)
def create_shoppingcart(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.goods_num -= instance.nums
        goods.save()

@receiver(post_delete, sender=ShoppingCart)
def delete_shoppingcart(sender, instance=None, created=False, **kwargs):
    instance.goods.goods_num += instance.nums
    instance.goods.save()
