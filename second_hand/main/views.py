# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours, PromotionsRegister, PromotionDays
from .shop_introduction import Store
from .shops_data_controller import ShopsDataController
from django.views.generic import ListView
import requests
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
            print(store.address)
            st = Store(store.id, store.name_store, store.country, store.city, store.address,
                       store.number_phone, store.number_stars, store.rating,
                       store.store_network, store.open_hours, store.promotion_days)
            list_shop_presentation.append(st)
            list_we = ['Адрес'] + st.list_week
        context['list_shop_presentation'] = list_shop_presentation
        context['list_we'] = list_we
        return context


# class Map(ListView):
#     template_name = 'main/map.html'
#     model = Stores
#     mo_12 = Stores.objects.all()
#     for store in mo_12:
#         store.save()

def map(request):
    respons = requests.get(url="https://mega-hand.by/magaziny/pervyj-magazin-megahend-v-minske/").json()
    a = respons.get('rates')
    print(a)
    return render(request, 'main/map.html')


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
    # a = ShopsDataController()
    # a.start()

    id_store = Stores.objects.get(id=id_store)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
                  id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours, id_store.promotion_days)
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
