from django.db import models
from django.urls import reverse
from pytils.translit import slugify
import datetime


class LinkSocNetworks(models.Model):  # ссылки на соц сети и официальный сайт
    link_home_page = models.URLField(blank=True)  # website
    inst = models.URLField(blank=True)
    vk = models.URLField(blank=True)
    tik_tok = models.URLField(blank=True)
    classmates = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)

    def __str__(self):
        return f'{self.link_home_page}'


class StoreNetwork(models.Model):  # сети магазинов
    name_network = models.CharField(max_length=50)  # название сети магазинов
    discount_card = models.CharField(max_length=50)  # дисконтная карта
    description = models.TextField()  # описание
    image = models.FileField(upload_to='store_network_logo', null=True, blank=True)
    links = models.ForeignKey(LinkSocNetworks, on_delete=models.CASCADE, null=True)  # id сети магазинов

    def __str__(self):
        return f'{self.name_network}'


class Gallery(models.Model):
    image = models.FileField(upload_to='shop_gallery')

    def __str__(self):
        return f'{self.image}'


class OpenHours(models.Model):  # рабочее время
    mon_st = models.DateTimeField(null=True, blank=True)
    mon_fn = models.DateTimeField(null=True, blank=True)
    tue_st = models.DateTimeField(null=True, blank=True)
    tue_fn = models.DateTimeField(null=True, blank=True)
    wed_st = models.DateTimeField(null=True, blank=True)
    wed_fn = models.DateTimeField(null=True, blank=True)
    thu_st = models.DateTimeField(null=True, blank=True)
    thu_fn = models.DateTimeField(null=True, blank=True)
    fri_st = models.DateTimeField(null=True, blank=True)
    fri_fn = models.DateTimeField(null=True, blank=True)
    sat_st = models.DateTimeField(null=True, blank=True)
    sat_fn = models.DateTimeField(null=True, blank=True)
    sun_st = models.DateTimeField(null=True, blank=True)
    sun_fn = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class PromotionsRegister(models.Model):  # все возможные акции и их процентное соотношение
    promotion_name = models.CharField(max_length=50)
    store_network = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    general_promotions = models.CharField(max_length=50, null=True, blank=True)  # УБРАТЬ blank=True, пересмотреть on_delete=models.CASCADE
    decoding = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True)
    discount_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.promotion_name}'


class PromotionDays(models.Model):  # дни акций
    monday = models.CharField(max_length=50, blank=True)
    tuesday = models.CharField(max_length=50, blank=True)
    wednesday = models.CharField(max_length=50, blank=True)
    thursday = models.CharField(max_length=50, blank=True)
    friday = models.CharField(max_length=50, blank=True)
    saturday = models.CharField(max_length=50, blank=True)
    sunday = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.id}'


class Stores(models.Model):  # магазины
    name_store = models.CharField(max_length=50)  # имя магазина
    country = models.CharField(max_length=50, blank=True)  # страна
    city = models.CharField(max_length=50)  # город
    address = models.CharField(max_length=50)  # адрес
    number_phone = models.CharField(max_length=17)  # номер телефона магазина
    number_stars = models.IntegerField(null=True, blank=True)  # количество звезд оставленных подьзователями
    rating = models.FloatField(null=True, blank=True)
    size = models.CharField(max_length=1, null=True, blank=True)
    store_network = models.ForeignKey(StoreNetwork, on_delete=models.CASCADE, null=True, blank=True)  # id сети магазинов которой он принадлежит
    open_hours = models.ForeignKey(OpenHours, on_delete=models.CASCADE, null=True, blank=True)  # id времени работы
    promotion_days = models.ForeignKey(PromotionDays, on_delete=models.CASCADE, null=True, blank=True)  # id скидок
    img = models.ForeignKey(Gallery, on_delete=models.PROTECT, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    link_shop = models.URLField(null=True, blank=True)
    #slug = models.SlugField(default='', null=False)

    def __str__(self):
        return f'{self.name_store}'

    def get_urls(self):
        return reverse('store', args=[self.id])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name_store)
    #     super().save(*args, **kwargs)


# class Reviews(models.Model):  # отзывы
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)  # id пользователя
#     name_store = models.ForeignKey(Stores, on_delete=models.CASCADE, null=True)  # id магазина
#     date = models.CharField()
#     reviews = models.CharField()
#     like = models.CharField()
#     dislike = models.CharField()


# """Пользователи"""
#
#
# class Users(models.Model):
#     name = models.CharField()
#     number_phone = models.CharField()
#     genders = models.CharField()
#     age = models.IntegerField()
#     img = models.CharField()
#     ip = models.CharField()
#     email = models.EmailField()
#
#
# class Elected(models.Model):  # избранное
#     store = models.ForeignKey(StoreNetwork, on_delete=models.CASCADE, null=True)  # id сети магазинов
#     replenishment = models.CharField()  # пополнение
#     description = models.CharField()  # описание