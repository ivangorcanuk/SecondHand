from django.db import models
from django.urls import reverse
from pytils.translit import slugify


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
    week_number = models.IntegerField()  # номер недели
    monday = models.CharField(max_length=20)
    tuesday = models.CharField(max_length=20)
    wednesday = models.CharField(max_length=20)
    thursday = models.CharField(max_length=20)
    friday = models.CharField(max_length=20)
    saturday = models.CharField(max_length=20)
    sunday = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}'


class PromotionsRegister(models.Model):  # все возможные акции и их процентное соотношение
    promotion_name = models.CharField(max_length=50)
    value = models.IntegerField()

    def __str__(self):
        return f'{self.promotion_name}'


class PromotionDays(models.Model):  # дни акций
    week_number = models.IntegerField()  # номер недели
    promotion_days = models.ManyToManyField(PromotionsRegister)  # id скидок
    # monday = models.CharField(max_length=50)
    # tuesday = models.CharField(max_length=50)
    # wednesday = models.CharField(max_length=50)
    # thursday = models.CharField(max_length=50)
    # friday = models.CharField(max_length=50)
    # saturday = models.CharField(max_length=50)
    # sunday = models.CharField(max_length=50)


class Stores(models.Model):  # магазины
    name_store = models.CharField(max_length=50)  # имя магазина
    country = models.CharField(max_length=50, blank=True)  # страна
    city = models.CharField(max_length=50)  # город
    area = models.CharField(max_length=50)  # район
    street = models.CharField(max_length=50, blank=True)  # улица
    house = models.CharField(max_length=50, blank=True)  # дом
    floor = models.CharField(max_length=50, blank=True)  # этаж
    number_phone = models.IntegerField()  # номер телефона магазина
    number_stars = models.IntegerField(null=True, blank=True)  # количество звезд оставленных подьзователями
    rating = models.FloatField(null=True, blank=True)
    store_network = models.ForeignKey(StoreNetwork, on_delete=models.CASCADE, null=True)  # id сети магазинов которой он принадлежит
    open_hours = models.ForeignKey(OpenHours, on_delete=models.CASCADE, null=True)  # id времени работы
    promotion_days = models.ForeignKey(PromotionDays, on_delete=models.CASCADE, null=True)  # id скидок
    #slug = models.SlugField(default='', null=False)

    def __str__(self):
        return f'{self.name_store} - {self.street}'

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