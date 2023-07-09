from django.db import models
from django.urls import reverse
from pytils.translit import slugify
import datetime


class StoreNetwork(models.Model):  # сети магазинов
    name_network = models.CharField(max_length=50)  # название сети магазинов
    discount_card = models.CharField(max_length=50)  # дисконтная карта
    description = models.TextField()  # описание

    def __str__(self):
        return f'{self.name_network}'


class LinkSocNetworks(models.Model):  # ссылки на соц сети и официальный сайт
    link = models.URLField(blank=True)
    inst = models.URLField(blank=True)
    vk = models.URLField(blank=True)
    tik_tok = models.URLField(blank=True)
    classmates = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    name_network = models.ForeignKey(StoreNetwork, on_delete=models.CASCADE, null=True)  # id сети магазинов


class OpenHours(models.Model):  # рабочее время
    mon_st = models.DateTimeField()
    mon_fn = models.DateTimeField()
    tue_st = models.DateTimeField()
    tue_fn = models.DateTimeField()
    wed_st = models.DateTimeField()
    wed_fn = models.DateTimeField()
    thu_st = models.DateTimeField()
    thu_fn = models.DateTimeField()
    fri_st = models.DateTimeField()
    fri_fn = models.DateTimeField()
    sat_st = models.DateTimeField()
    sat_fn = models.DateTimeField()
    sun_st = models.DateTimeField()
    sun_fn = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'


class PromotionsRegister(models.Model):  # все возможные акции и их процентное соотношение
    promotion_name = models.CharField(max_length=50)
    value = models.IntegerField()

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


class Stores(models.Model):  # магазины
    name_store = models.CharField(max_length=50)  # имя магазина
    country = models.CharField(max_length=50, blank=True)  # страна
    city = models.CharField(max_length=50)  # город
    address = models.CharField(max_length=50)  # адрес
    number_phone = models.IntegerField()  # номер телефона магазина
    number_stars = models.IntegerField(null=True, blank=True)  # количество звезд оставленных подьзователями
    rating = models.FloatField(null=True, blank=True)
    store_network = models.ForeignKey(StoreNetwork, on_delete=models.CASCADE, null=True)  # id сети магазинов которой он принадлежит
    open_hours = models.ForeignKey(OpenHours, on_delete=models.CASCADE, null=True)  # id времени работы
    promotion_days = models.ForeignKey(PromotionDays, on_delete=models.CASCADE, null=True)  # id скидок
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