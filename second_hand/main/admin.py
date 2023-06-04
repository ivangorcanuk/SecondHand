from django.contrib import admin
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours, PromotionDays, PromotionsRegister


@admin.register(StoreNetwork)
class StoreNetwork(admin.ModelAdmin):
    list_display = ['id', 'name_network', 'discount_card', 'description']
    #list_editable = ['name_network']  # список изменения полей

    def __str__(self):
        return f'{self.name_network} - {self.discount_card} - {self.description}'


@admin.register(LinkSocNetworks)
class LinkSocNetworks(admin.ModelAdmin):
    list_display = ['link', 'inst', 'vk', 'tik_tok', 'classmates', 'facebook', 'telegram']
    #list_editable = ['discount_card', 'description']  # список изменения полей

    def __str__(self):
        return f'{self.link} - {self.inst} - {self.vk} - {self.tik_tok} - {self.classmates} - {self.facebook} - {self.telegram}'


@admin.register(Stores)
class Stores(admin.ModelAdmin):
    list_display = ['name_store', 'country', 'city', 'area', 'street',
                    'house', 'store_network_id', 'open_hours']
    #list_editable = ['area', 'rating']  # список изменения полей

    def __str__(self):
        return f'{self.name_store} - {self.city} - {self.area} - {self.street_house} - {self.number_phone}'


@admin.register(OpenHours)
class OpenHours(admin.ModelAdmin):
    list_display = ['week_number', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
    #list_editable = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']  # список изменения полей

    def __str__(self):
        return f'{self.week_number} - {self.monday} - {self.tuesday} - {self.wednesday} - ' \
               f'{self.thursday} - {self.friday} - {self.saturday} - {self.sunday}'


@admin.register(PromotionDays)
class PromotionDays(admin.ModelAdmin):
    list_display = ['store', 'week_number', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
    #list_editable = ['number_stars', 'rating']  # список изменения полей

    def __str__(self):
        return f'{self.store} - {self.week_number} - {self.monday} - {self.tuesday} - {self.wednesday} - ' \
               f'{self.thursday} - {self.friday} - {self.saturday} - {self.sunday}'


@admin.register(PromotionsRegister)
class PromotionsRegister(admin.ModelAdmin):
    list_display = ['id', 'promotion_name', 'value']
    #list_editable = ['number_stars', 'rating']  # список изменения полей

    def __str__(self):
        return f'{self.promotion_name} - {self.value}'