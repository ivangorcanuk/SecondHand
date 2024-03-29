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
from django.views.generic import ListView, DetailView, FormView
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import requests
import re
from datetime import datetime, date, timedelta
from .forms import SearchForm, FiltersForm, list_sales, list_discounts
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# создать переменную объекта класса Базы данных и польлозоваться ею во всех классах или в каждом классе создавать свою переменную


class HomePage(ListView):
    model = Stores
    template_name = 'main/index.html'
    context_object_name = 'stor'


class BasicData:
    form_search = SearchForm()
    form_filters = FiltersForm()
    list_social_discounts = ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%']
    dikt_networks = {'checkbox_network_moda_max': 'Мода Макс',
                     'checkbox_network_economy_city': 'Эконом Сити',
                     'checkbox_network_adzenne': 'Адзенне',
                     'checkbox_network_megahand': 'Мегахенд'}
    dikt_sizes = {'checkbox_size_S': 'S',
                  'checkbox_size_M': 'M',
                  'checkbox_size_L': 'L'}

    def convert_to_view_item(self, base_shop):
        list_shop_presentation = list()
        for shop in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
                               shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
                               shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
            list_shop_presentation.append(st)
        return list_shop_presentation


class Catalog(BasicData, ListView):
    model = Stores
    template_name = 'main/catalog.html'
    context_object_name = 'stor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = True
        context['form_search'] = self.form_search
        context['form_filters'] = self.form_filters
        context['list_social_discounts'] = self.list_social_discounts
        context['list_shops_presentation'] = self.convert_to_view_item(context['stor'])
        context['today'] = datetime.weekday(date.today())
        # a = ShopsDataController()
        # a.start()
        return context


class SearchHandlerView(Catalog):
    form = None
    search = None

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(request.GET)  # попробовать вытянуть из формы запрос и убрать вторую переменную
        self.search = request.GET['search']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_shops_presentation = self.handle_search(self.search, context['list_shops_presentation'])
        context['form_search'] = self.form
        context['list_shops_presentation'] = list_shops_presentation
        return context

    def handle_search(self, search, list_shops):
        list_shop_presentation = list()
        for shop in list_shops:
            name_store = shop.name_store
            address = shop.address
            if search.upper() in name_store.upper() or search.upper() in address.upper():
                list_shop_presentation.append(shop)
        return list_shop_presentation


class FilterHandlerView(Catalog):
    form = None

    def get(self, request, *args, **kwargs):
        self.form = FiltersForm(request.GET)  # попробовать вытянуть из формы запрос и убрать вторую переменную
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_shops_presentation = self.handle_filtering(self.form.data, context['list_shops_presentation'])
        context['form_filters'] = self.form
        context['list_shops_presentation'] = list_shops_presentation
        return context

    def handle_filtering(self, filter_data, list_shops):
        print(filter_data)
        list_networks = list()
        list_sizes = list()
        for key, value in filter_data.items():
            if 'checkbox_network' in key:
                list_networks.append(self.dikt_networks[key])
            if 'checkbox_size' in key:
                list_sizes.append(self.dikt_sizes[key])

        if list_networks:  # если заполнен
            list_shops = self.filter_by_shop_network(list_networks, list_shops)

        if list_sizes:
            list_shops = self.filter_by_shop_size(list_sizes, list_shops)

        if filter_data['combobox_sales'] != 'Все скидки':
            list_shops = self.processes_sale(list_shops, filter_data['combobox_sales'], filter_data['date'])

        if filter_data['combobox_discounts'] != 'Все акции':
            list_shops = self.processes_sale(list_shops, filter_data['combobox_discounts'], filter_data['date'])

        return list_shops

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
        discounts = PromotionsRegister.objects.filter(general_promotions=discount)
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


class SocialDiscountsView(Catalog):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs.get('discount'))
        list_shops_presentation = self.handle_social_discount(self.kwargs.get('discount'), context['list_shops_presentation'])
        context['list_shops_presentation'] = list_shops_presentation
        return context

    def handle_social_discount(self, discount, list_shops):
        dikt_similarity_discounts = {
            'Пенсионерам': ['День сеньора', 'Социальная скидка'],
            'Студентам': ['Скидка для студентов'],
            'Детям': ['Детский день'],
            'Семейные': ['3я вещь в подарок', '4я вещь в подарок'],
            'На всё от 80%': ['9.90', '12.90', '-80%', '-85%', '-90%', '-95%', 'Всё по 1 рублю',
                              'Всё по 2 рубля', 'Всё по 4 рубля']
        }
        list_temp = list()
        discounts_all = PromotionsRegister.objects.all()
        for promotion in discounts_all:
            if promotion.general_promotions in dikt_similarity_discounts[discount]:
                for shop in list_shops:
                    for j in range(datetime.weekday(date.today()), len(shop.list_promotion)):
                        list_id = shop.list_promotion[j].split('*')
                        if str(promotion.id) in list_id:
                            list_temp.append(shop)
        return list_temp


# class Cataloge:
#     db = DBInteractionHandler()
#     form_search = SearchForm()
#     form_filters = FiltersForm()
#     data = {
#         'search': True,
#         'form_search': form_search,
#         'form_filters': form_filters,
#         'list_social_discounts': ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%'],
#     }
#     dikt_networks = {'checkbox_network_moda_max': 'Мода Макс',
#                      'checkbox_network_economy_city': 'Эконом Сити',
#                      'checkbox_network_adzenne': 'Адзенне',
#                      'checkbox_network_megahand': 'Мегахенд'}
#     dikt_sizes = {'checkbox_size_S': 'S',
#                   'checkbox_size_M': 'M',
#                   'checkbox_size_L': 'L'}
#
#     def __init__(self):
#         self.base_shop = self.db.base_shop
#         self.list_shops = self.convert_to_view_item(self.base_shop)
#         self.discounts = self.db.base_sale
#
#     def catalog(self, request):
#         self.data['form_filters'] = self.form_filters
#         self.data['list_shops_presentation'] = self.list_shops
#         self.data['today'] = datetime.weekday(date.today())
#         #self.data['bool'] = False
#         # a = ShopsDataController()
#         # a.start()
#         return render(request, 'main/catalog.html', context=self.data)
#
#     def handle_search(self, request):
#         form = SearchForm(request.GET)
#         print(request.GET['search'])
#         if form.is_valid():
#             search_str = request.GET['search']
#             list_shop_presentation = list()
#             for shop in self.list_shops:
#                 name_store = shop.name_store
#                 address = shop.address
#                 if search_str.upper() in name_store.upper() or search_str.upper() in address.upper():
#                     list_shop_presentation.append(shop)
#             self.data['form_search'] = form
#             self.data['list_shops_presentation'] = list_shop_presentation
#             return render(request, 'main/catalog.html', context=self.data)
#
#     def handle_filtering(self, request):
#         print(request.GET)
#         list_shops_sorted = self.list_shops
#         list_networks = list()
#         list_sizes = list()
#         week_day = str()
#         form = FiltersForm(request.GET)
#         if form.is_valid():
#             for key, value in request.GET.items():
#                 if 'checkbox_network' in key:
#                     list_networks.append(self.dikt_networks[key])
#                 if 'checkbox_size' in key:
#                     list_sizes.append(self.dikt_sizes[key])
#
#             if list_networks:  # если заполнен
#                 list_shops_sorted = self.filter_by_shop_network(list_networks, list_shops_sorted)
#
#             if list_sizes:
#                 list_shops_sorted = self.filter_by_shop_size(list_sizes, list_shops_sorted)
#
#             if request.GET['combobox_sales'] != 'Все скидки':
#                 list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_sales'], request.GET['date'])
#
#             if request.GET['combobox_discounts'] != 'Все акции':
#                 list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_discounts'], request.GET['date'])
#
#         self.data['form_filters'] = form
#         self.data['list_shops_presentation'] = list_shops_sorted
#
#         return render(request, 'main/catalog.html', context=self.data)
#
#     def filter_by_shop_network(self, list_networks, list_shops_sorted):
#         list_temp = list()
#         for shop in list_shops_sorted:
#             if shop.name_store in list_networks:
#                 list_temp.append(shop)
#         return list_temp
#
#     def filter_by_shop_size(self, list_shop_size, list_shops_sorted):
#         list_temp = list()
#         for shop in list_shops_sorted:
#             if shop.size in list_shop_size:
#                 list_temp.append(shop)
#         return list_temp
#
#     def processes_sale(self, list_shops_sorted, discount, week_day):
#         discounts = self.db.get_sale_similar(discount)
#         list_temp = list()
#         list_days = [i for i in range(datetime.weekday(date.today()), 7)]
#
#         if week_day != '':
#             week_day = datetime.strptime(week_day, '%Y-%m-%d')
#             list_days = [date.weekday(week_day)]
#
#         for stor in list_shops_sorted:
#             for j in list_days:
#                 list_id = stor.list_promotion[j].split('*')
#                 for disc in discounts:
#                     if str(disc.id) in list_id:
#                         list_temp.append(stor)
#                         break
#         return list_temp
#
#     def convert_to_view_item(self, base_shop):
#         list_shop_presentation = list()
#         for shop in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
#             st = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
#                                shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
#                                shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
#             list_shop_presentation.append(st)
#         return list_shop_presentation
#
#     def pensioners(self, request, discount: str):
#         dikt_similarity_discounts = {
#             'Пенсионерам': ['День сеньора', 'Социальная скидка'],
#             'Студентам': ['Скидка для студентов'],
#             'Детям': ['Детский день'],
#             'Семейные': ['3я вещь в подарок', '4я вещь в подарок'],
#             'На всё от 80%': ['9.90', '12.90', '-80%', '-85%', '-90%', '-95%', 'Всё по 1 рублю',
#                               'Всё по 2 рубля', 'Всё по 4 рубля']
#         }
#         list_temp = list()
#         for promotion in self.discounts:
#             if promotion.general_promotions in dikt_similarity_discounts[discount]:
#                 for shop in self.list_shops:
#                     for j in range(datetime.weekday(date.today()), len(shop.list_promotion)):
#                         list_id = shop.list_promotion[j].split('*')
#                         if str(promotion.id) in list_id:
#                             list_temp.append(shop)
#         self.data['form_search'] = self.form_search
#         self.data['form_filters'] = self.form_filters
#         self.data['list_shops_presentation'] = list_temp
#         return render(request, 'main/catalog.html', context=self.data)


class Store(DetailView):
    model = Stores
    template_name = 'main/store.html'
    context_object_name = 'stor'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = context['stor']
        context['store'] = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
                                         shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
                                         shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
        context['isPhotoButtonClicked'] = False
        context['today']: StoreViewItem.list_week[datetime.weekday(date.today())]
        context['data'] = json.dumps(
            [
                {
                    'name': context['store'].name_store,
                    'address': context['store'].address,
                    'phone': context['store'].number_phone,
                    'time_work': context['store'].opening_hours_today_text,
                    'lat': context['store'].latitude,
                    'lon': context['store'].longitude,
                }
            ]
        )
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get(self, request, *args, **kwargs):
        print('qwe')
        queryset = False
        return JsonResponse({"isPhotoButtonClicked": queryset})


class Map(ListView):
    model = Stores
    template_name = 'main/map.html'
    context_object_name = 'store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_shop_presentation = list()
        for shop in context['store']:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = StoreViewItem(shop.id, shop.name_store, shop.country, shop.city, shop.address, shop.number_phone,
                               shop.number_stars, shop.rating, shop.size, shop.store_network, shop.open_hours,
                               shop.promotion_days, shop.img, shop.latitude, shop.longitude, shop.link_shop)
            list_shop_presentation.append(st)

        list_shops_all = list()
        list_shops_modamax = list()
        list_shops_economcity = list()
        list_shops_adzene = list()
        list_shops_megahend = list()
        for shop in list_shop_presentation:
            dict_temp = dict()
            dict_temp['lat'] = shop.latitude
            dict_temp['lon'] = shop.longitude
            dict_temp['name'] = shop.name_store
            dict_temp['address'] = shop.address
            dict_temp['phone'] = shop.number_phone
            dict_temp['link'] = shop.link
            dict_temp['time_work'] = shop.opening_hours_today_text

            list_shops_all.append(dict_temp)
            if shop.store_network.name_network == 'Мода Макс':
                list_shops_modamax.append(dict_temp)
            elif shop.store_network.name_network == 'Эконом Сити':
                list_shops_economcity.append(dict_temp)
            elif shop.store_network.name_network == 'Адзенне':
                list_shops_adzene.append(dict_temp)
            elif shop.store_network.name_network == 'Мегахенд':
                list_shops_megahend.append(dict_temp)
        context['data'] = json.dumps([list_shops_all, list_shops_modamax,
                                      list_shops_economcity, list_shops_adzene, list_shops_megahend])

        return context


class About(ListView):
    model = Stores
    template_name = 'main/about.html'
    context_object_name = 'stor'


class News(ListView):
    model = Stores
    template_name = 'main/news.html'
    context_object_name = 'stor'
