from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class Goods(models.Model):
    """
    商品
    """
    category = models.CharField(default="踩的", max_length=30,
                                choices=(("踩的", "踩的"), ("穿的", "穿的"), ("戴的", "戴的")), verbose_name="类别", help_text="类别")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    price = models.FloatField(default=0, verbose_name="价格")
    gender = models.CharField(max_length=10, choices=(("male", "男的"), ("female", "女的"), ("neutral", "男女同款")),
                              default="female", verbose_name="性别")
    goods_desc = UEditorField(verbose_name="内容", width=800, height=300, default='')
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    is_sale = models.BooleanField(default=False, verbose_name="是否优惠")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodCS(models.Model):
    """
    商品色码
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="cs")
    goods_size = models.CharField(max_length=10, choices=(("35", "35"), ("36", "36"), ("37", "37"),
                                                         ("38", "38"), ("39", "39"), ("40", "40"),
                                                         ("41", "41"), ("42", "42"), ("43", "43"),
                                                         ("44", "44"), ("45", "45"), ("S", "S"),
                                                         ("M", "M"), ("L", "L"), ("XL", "XL"),
                                                         ("均码", "均码")),
                                  verbose_name="尺码")
    goods_color = models.CharField(max_length=10, null=True, blank=True, verbose_name="颜色")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品色码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.goods.name) + ' ' + str(self.goods_size) + ' ' + self.goods_color


class GoodImage(models.Model):
    """
    商品详情图
    """
    cs = models.ForeignKey(GoodCS, verbose_name="商品色码", related_name="img")
    image = models.ImageField(upload_to="goods/images/", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cs.goods.name


class Banner(models.Model):
    """
    轮播图
    """
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    link = models.CharField(null=True, blank=True, verbose_name="链接", max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.image)
