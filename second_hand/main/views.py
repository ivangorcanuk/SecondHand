# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours, PromotionsRegister, PromotionDays, Gallery
from .shop_introduction import Store
from .shops_data_controller import ShopsDataController
from django.views.generic import ListView
import requests
import re
from datetime import datetime, date, timedelta
from .forms import SearchForm
from django.db.models import Q

# придумать хитрый механизм для отображения рабочего времени по дням недели!
# добавить уникальность open_hours


def index(request):
    return render(request, 'main/index.html')


def catalog(request):
    list_shop_presentation = list()  # список представления магазинов
    form = SearchForm(request.POST)

    base_shop = Stores.objects.all()
    for store in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
        #print(store.address)
        st = Store(store.id, store.name_store, store.country, store.city, store.address,
                   store.number_phone, store.number_stars, store.rating,
                   store.store_network, store.open_hours, store.promotion_days)
        list_shop_presentation.append(st)

    list_discounts = list()
    base_sale = PromotionsRegister.objects.values_list('general_promotions', flat=True)
    for discount in base_sale:
        if discount is not None and len(discount) > 4 and discount != 'Выходной':
            list_discounts.append(discount)
    list_discounts = list(set(list_discounts))

    data = {
        'form': form,
        'list_shop_presentation': list_shop_presentation,
        'name_network': ['Мода Макс', 'Эконом Сити', 'Адзенне', 'Мегахенд'],
        'cities': ['Минск'],
        'sizes': ['S', 'M', 'L'],
        'sales': ['-20%', '-40%', '-60%', '-80%'],
        'discounts': list_discounts,
        'list_social_discounts': ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%'],
    }

    if request.method == 'POST':
        if form.is_valid():
            name = request.POST['search']
            list_stor = Stores.objects.filter(Q(name_store__icontains=name) | Q(address__icontains=name))
            list_shop_presentation = list()
            for store in list_stor:
                st = Store(store.id, store.name_store, store.country, store.city, store.address,
                           store.number_phone, store.number_stars, store.rating,
                           store.store_network, store.open_hours, store.promotion_days)
                list_shop_presentation.append(st)

            data['list_shop_presentation'] = list_shop_presentation

            return render(request, 'main/catalog.html', context=data)

    if request.method == 'GET':
        print('asd')
        print(request.GET.get('fruits'))
        print(request.GET.get('store_network'))
        print(request.GET.get('shop_size'))
        print(request.GET.get('sales'))
        print(request.GET.get('discounts'))
        # list_stor = Stores.objects.filter(Q(name_store__icontains=name) | Q(address__icontains=name))
        # list_shop_presentation = list()
        # for store in list_stor:
        #     st = Store(store.id, store.name_store, store.country, store.city, store.address,
        #                store.number_phone, store.number_stars, store.rating,
        #                store.store_network, store.open_hours, store.promotion_days)
        #     list_shop_presentation.append(st)
        #
        # data['list_shop_presentation'] = list_shop_presentation
        #
        # return render(request, 'main/catalog.html', context=data)

    return render(request, 'main/catalog.html', context=data)


# class Index(ListView):
#     template_name = 'main/index.html'
#     model = Stores
#
#     def get_context_data(self, **kwargs):
#         context = super(Index, self).get_context_data(**kwargs)
#         list_shop_presentation = list()  # список представления магазинов
#         base_shop = Stores.objects.all()
#         for store in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
#             print(store.address)
#             st = Store(store.id, store.name_store, store.country, store.city, store.address,
#                        store.number_phone, store.number_stars, store.rating,
#                        store.store_network, store.open_hours, store.promotion_days)
#             list_shop_presentation.append(st)
#         context['list_shop_presentation'] = list_shop_presentation
#         return context


# class Map(ListView):
#     template_name = 'main/map.html'
#     model = Stores
#     mo_12 = Stores.objects.all()
#     for store in mo_12:
#         store.save()

def map(request):
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
        'img': id_store,
    }
    return render(request, 'main/store.html', context=data)


def all_shop(request):
    # id_store = Stores.objects.get(id=3)
    # store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
    #               id_store.number_phone, id_store.number_stars, id_store.rating,
    #               id_store.store_network, id_store.open_hours)
    # data = {
    #     'store': store,
    # }
    return render(request, 'main/all_shop.html')


def login(request):
    return render(request, 'main/login.html')


def about(request):
    return render(request, 'main/about.html')


def news(request):
    return render(request, 'main/news.html')


def forum(request):
    return render(request, 'main/forum.html')
