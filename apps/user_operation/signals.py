#!/usr/bin/env python
__author__ = 'Albino'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


# 完成后在apps中设置ready函数
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods.goods
        goods.fav_num += 1
        goods.save()

@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    instance.goods.goods.fav_num -= 1
    instance.goods.goods.save()