# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
import json
from django.shortcuts import render
from .db_interaction_handler import DBInteractionHandler
from .shop_introduction import StoreViewItem
from .shops_data_controller import ShopsDataController
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
import requests
import re
from datetime import datetime, date, timedelta
from .forms import SearchForm, FiltersForm, list_sales, list_discounts
from django.db.models import Q

# создать переменную объекта класса Базы данных и польлозоваться ею во всех классах или в каждом классе создавать свою переменную


def index(request):
    return render(request, 'main/index.html')


class Catalog:
    db = DBInteractionHandler()
    form_search = SearchForm()
    form_filters = FiltersForm()
    data = {
        'search': True,
        'form_search': form_search,
        'form_filters': form_filters,
        'list_social_discounts': ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%'],
    }
    dikt_networks = {'checkbox_network_moda_max': 'Мода Макс',
                     'checkbox_network_economy_city': 'Эконом Сити',
                     'checkbox_network_adzenne': 'Адзенне',
                     'checkbox_network_megahand': 'Мегахенд'}
    dikt_sizes = {'checkbox_size_S': 'S',
                  'checkbox_size_M': 'M',
                  'checkbox_size_L': 'L'}

    def __init__(self):
        self.base_shop = self.db.base_shop
        self.list_shops = self.convert_to_view_item(self.base_shop)
        self.discounts = self.db.base_sale

    def catalog(self, request):
        self.data['form_filters'] = self.form_filters
        self.data['list_shops_presentation'] = self.list_shops
        return render(request, 'main/catalog.html', context=self.data)

    def handle_search(self, request):
        form = SearchForm(request.GET)
        print(request.GET['search'])
        if form.is_valid():
            search_str = request.GET['search']
            list_shop_presentation = list()
            for shop in self.list_shops:
                name_store = shop.name_store
                address = shop.address
                if search_str.upper() in name_store.upper() or search_str.upper() in address.upper():
                    list_shop_presentation.append(shop)
            self.data['form_search'] = form
            self.data['list_shops_presentation'] = list_shop_presentation
            return render(request, 'main/catalog.html', context=self.data)

    def handle_filtering(self, request):
        print(request.GET)
        list_shops_sorted = self.list_shops
        list_networks = list()
        list_sizes = list()
        week_day = str()
        form = FiltersForm(request.GET)
        if form.is_valid():
            for key, value in request.GET.items():
                if 'checkbox_network' in key:
                    list_networks.append(self.dikt_networks[key])
                if 'checkbox_size' in key:
                    list_sizes.append(self.dikt_sizes[key])

            if list_networks:  # если заполнен
                list_shops_sorted = self.filter_by_shop_network(list_networks, list_shops_sorted)

            if list_sizes:
                list_shops_sorted = self.filter_by_shop_size(list_sizes, list_shops_sorted)

            if request.GET['combobox_sales'] != 'Все скидки':
                list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_sales'], request.GET['date'])

            if request.GET['combobox_discounts'] != 'Все акции':
                list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_discounts'], request.GET['date'])

        self.data['form_filters'] = form
        self.data['list_shops_presentation'] = list_shops_sorted

        return render(request, 'main/catalog.html', context=self.data)

    def filter_by_shop_network(self, list_networks, list_shops_sorted):
        list_temp = list()
        for shop in list_shops_sorted:
            if shop.name_store in list_networks:
                list_temp.append(shop)
        return list_temp

    def filter_by_shop_size(self, list_shop_size, list_shops_sorted):
        list_temp = list()
        for shop in list_shops_sorted:
            if shop.size in list_shop_size:
                list_temp.append(shop)
        return list_temp

    def processes_sale(self, list_shops_sorted, discount, week_day):
        discounts = self.db.get_sale_similar(discount)
        list_temp = list()
        list_days = [i for i in range(datetime.weekday(date.today()), 7)]

        if week_day != '':
            week_day = datetime.strptime(week_day, '%Y-%m-%d')
            list_days = [date.weekday(week_day)]

        for stor in list_shops_sorted:
            for j in list_days:
                list_id = stor.list_promotion[j].split('*')
                for disc in discounts:
                    if str(disc.id) in list_id:
                        list_temp.append(stor)
                        break
        return list_temp

    def convert_to_view_item(self, base_shop):
        list_shop_presentation = list()
        for shop in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
                               shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
                               shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
            list_shop_presentation.append(st)
        return list_shop_presentation

    def pensioners(self, request, discount: str):
        dikt_similarity_discounts = {
            'Пенсионерам': ['День сеньора', 'Социальная скидка'],
            'Студентам': ['Скидка для студентов'],
            'Детям': ['Детский день'],
            'Семейные': ['3я вещь в подарок', '4я вещь в подарок'],
            'На всё от 80%': ['-80%', '-85%', '-90%', '-95%', 'Всё по 1 рублю',
                              'Всё по 2 рубля', 'Всё по 4 рубля']
        }
        list_temp = list()
        for promotion in self.discounts:
            if promotion.general_promotions in dikt_similarity_discounts[discount]:
                for shop in self.list_shops:
                    for j in range(datetime.weekday(date.today()), len(shop.list_promotion)):
                        list_id = shop.list_promotion[j].split('*')
                        if str(promotion.id) in list_id:
                            list_temp.append(shop)
        self.data['form_search'] = self.form_search
        self.data['form_filters'] = self.form_filters
        self.data['list_shops_presentation'] = list_temp
        return render(request, 'main/catalog.html', context=self.data)


class Stor:
    db = DBInteractionHandler()

    def __init__(self):
        self.id_store = int()
        self.store = None
        self.data = dict()

    def stor(self, request, id_store: int):
        # a = ShopsDataController()
        # a.start()
        self.id_store = id_store
        shop = self.db.get_shop(id_store)
        store = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
                              shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
                              shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
        print(self.id_store)
        self.data = {
            'store': store,
            'img': id_store,
            'photo': True,
        }
        return render(request, 'main/store.html', context=self.data)

    def shop_map(self, request):
        if request.GET['photo_or_map'] == 'Карта':
            self.data['photo'] = False
        else:
            self.data['photo'] = True
        self.data['data'] = json.dumps(
            [
                {
                    'lat': self.data['store'].latitude,
                    'lon': self.data['store'].longitude,
                }
            ]
        )
        return render(request, 'main/store.html', context=self.data)


class Map:
    db = DBInteractionHandler()

    def __init__(self):
        self.all_shop = self.db.base_shop

    def map(self, request):
        data = dict()
        list_geolocation = list()
        for i in range(5):
            list_geolocation.append(self.get_geolocation(i))
        data['data'] = json.dumps(list_geolocation)
        return render(request, 'main/map.html', context=data)

    def get_geolocation(self, condition):
        list_temp = list()
        if condition == 1:
            condition = 'Мода Макс'
        elif condition == 2:
            condition = 'Эконом Сити'
        elif condition == 3:
            condition = 'Адзенне'
        elif condition == 4:
            condition = 'Мегахенд'
        else:
            condition = 'Все'

        for shop in self.all_shop:
            dict_temp = dict()
            if condition == shop.name_store:
                dict_temp['lat'] = shop.latitude
                dict_temp['lon'] = shop.longitude
                dict_temp['name'] = shop.name_store
                dict_temp['address'] = shop.address
                dict_temp['number_phone'] = shop.number_phone
                list_temp.append(dict_temp)
            elif condition == 'Все':
                dict_temp['lat'] = shop.latitude
                dict_temp['lon'] = shop.longitude
                dict_temp['name'] = shop.name_store
                dict_temp['address'] = shop.address
                dict_temp['number_phone'] = shop.number_phone
                list_temp.append(dict_temp)
        return list_temp


def about(request):
    form_search = SearchForm()
    form_filters = FiltersForm()
    data = {
        'form_search': form_search,
        'form_filters': form_filters,
        'list_name_network': ['Мода Макс', 'Эконом Сити', 'Адзенне', 'Мегахенд'],
    }
    return render(request, 'main/about.html', context=data)


def news(request):
    return render(request, 'main/news.html')

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


# class Store(ListView):
#     template_name = 'main/store.html'
#     model = Stores
#
#     def get_context_data(self, **kwargs):
#         context = super(Store, self).get_context_data(**kwargs)
#         context['set'] = OpenHours.objects.all()
#         cur = datetime.now()
#         return context