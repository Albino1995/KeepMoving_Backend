#!/usr/bin/env python
__author__ = 'Albino'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# 获取UserProfile
User = get_user_model()

# 完成后在apps中设置ready函数
@receiver(post_save, sender=User)
def create_make_password(sender, instance=None, created=False, **kwargs):
    """
    # 将传送的密码加密
    """
    if created:
        # instance相当于user
        password = instance.password
        instance.set_password(password)
        instance.save()