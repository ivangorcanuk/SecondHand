# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours, PromotionsRegister, PromotionDays
from .shop_introduction import Store
from django.views.generic import ListView
import re
from datetime import datetime, date, timedelta

# придумать хитрый механизм для отображения рабочего времени по дням недели!
# добавить уникальность open_hours
class Index(ListView):
    template_name = 'main/index.html'
    model = Stores

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        list_shop_presentation = list()  # список представления магазинов
        base_shop = Stores.objects.all()
        for store in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = Store(store.id, store.name_store, store.country, store.city, store.address,
                       store.number_phone, store.number_stars, store.rating,
                       store.store_network, store.open_hours)
            list_shop_presentation.append(st)
        context['list_shop_presentation'] = list_shop_presentation
        return context


class Map(ListView):
    template_name = 'main/map.html'
    model = Stores
    # mo_12 = Stores.objects.all()
    # for store in mo_12:
    #     store.save()


# class Store(ListView):
#     template_name = 'main/store.html'
#     model = Stores
#
#     def get_context_data(self, **kwargs):
#         context = super(Store, self).get_context_data(**kwargs)
#         context['set'] = OpenHours.objects.all()
#         cur = datetime.now()
#         return context


def stor(request, id_store: int):
    dict_week = {
        'Пн': [],
        'Вт': [],
        'Ср': [],
        'Чт': [],
        'Пт': [],
        'Сб': [],
        'Вс': [],
    }
    dict_many = {
            'Пн': ['39.90', 'Семейные дни', 'День сеньора'],
            'Вт': ['29.90', 'Семейные дни', ''],
            'Ср': ['19.90', '', ''],
            'Чт': ['9.90', '', ''],
            'Пт': ['59.90', 'Новый товар', ''],
            'Сб': ['54.90', '', ''],
            'Вс': ['49.90', '', ''],
                }
    stock_all = PromotionsRegister.objects.all()

    for key, value in dict_many.items():
        i = 0
        j = 0
        id_str = str()
        while True:
            if i == len(stock_all):
                i = 0
            if value[j] == stock_all[i].promotion_name:
                id_str += str(stock_all[i].id)
                if j < len(value) - 1:
                    j += 1
                    if value[j] == '':
                        break
                else:
                    break
                id_str += '*'
            i += 1
        dict_week[key] = id_str
    for key, value in dict_week.items():
        print(key, value)
    stores = Stores.objects.all()
    for sh in stores:
        if sh.id == 10:
            sh.promotion_days.monday = dict_week['Пн']
            sh.promotion_days.tuesday = dict_week['Вт']
            sh.promotion_days.wednesday = dict_week['Ср']
            sh.promotion_days.thursday = dict_week['Чт']
            sh.promotion_days.friday = dict_week['Пт']
            sh.promotion_days.saturday = dict_week['Сб']
            sh.promotion_days.sunday = dict_week['Вс']
            sh.promotion_days.save()

    id_store = Stores.objects.get(id=id_store)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
                  id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours)
    data = {
        'store': store,
    }
    return render(request, 'main/store.html', context=data)


def search(request):
    id_store = Stores.objects.get(id=3)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
                  id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours)
    data = {
        'store': store,
    }
    return render(request, 'main/search.html', context=data)


def login(request):
    return render(request, 'main/login.html')


def register(request):
    return render(request, 'main/register.html')
