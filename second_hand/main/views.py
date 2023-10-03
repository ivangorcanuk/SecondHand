# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours, PromotionsRegister, PromotionDays, Gallery
from .shop_introduction import StoreViewItem
from .shops_data_controller import ShopsDataController
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
import requests
import re
from datetime import datetime, date, timedelta
from .forms import SearchForm, FiltersForm, list_sales, list_discounts
from django.db.models import Q

# придумать хитрый механизм для отображения рабочего времени по дням недели!
# добавить уникальность open_hours


def index(request):
    return render(request, 'main/index.html')


class Catalog:
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
        self.base_shop = Stores.objects.all()
        self.list_shops = self.convert_to_view_item(self.base_shop)
        self.discounts = PromotionsRegister.objects.all()

    def catalog(self, request):
        self.data['form_filters'] = self.form_filters
        self.data['list_shop_presentation'] = self.list_shops
        return render(request, 'main/catalog.html', context=self.data)

    def handle_search(self, request):
        form = SearchForm(request.GET)
        if form.is_valid():
            search_str = request.GET['search']
            list_shop_presentation = list()
            for shop in self.list_shops:
                name_store = shop.name_store
                address = shop.address
                if search_str.upper() in name_store.upper() or search_str.upper() in address.upper():
                    list_shop_presentation.append(shop)
            self.data['form_search'] = form
            self.data['list_shop_presentation'] = list_shop_presentation
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

            if request.GET['date'] != '':
                week_day = str(date.weekday(date.today()))

            if request.GET['combobox_sales'] != 'Все скидки':
                list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_sales'], week_day)

            if request.GET['combobox_discounts'] != 'Все акции':
                list_shops_sorted = self.processes_sale(list_shops_sorted, request.GET['combobox_discounts'], week_day)

        self.data['form_filters'] = form
        self.data['list_shop_presentation'] = list_shops_sorted

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
        discounts = PromotionsRegister.objects.filter(general_promotions=discount)
        list_temp = list()
        list_days = [i for i in range(datetime.weekday(date.today()), 7)]

        if week_day != '':
            list_days = [int(week_day) - 1]
        print(list_days)
        for stor in list_shops_sorted:
            for j in list_days:
                list_id = stor.list_promotion[j].split('*')
                for disc in discounts:
                    if str(disc.id) in list_id:
                        list_temp.append(stor)
                        break
        # for i in discounts:
        #     for stor in list_shops_sorted:
        #         if week_day == '':
        #             for j in range(datetime.weekday(date.today()), len(stor.list_promotion)):
        #                 list_id = stor.list_promotion[j].split('*')
        #                 if str(i.id) in list_id:
        #                     list_temp.append(stor)
        #         else:
        #             list_id = stor.list_promotion[int(week_day)].split('*')
        #             if str(i.id) in list_id:
        #                 list_temp.append(stor)
        return list_temp

    def convert_to_view_item(self, base_shop):
        list_shop_presentation = list()
        for store in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = StoreViewItem(store.id, store.name_store, store.country, store.city, store.address,
                               store.number_phone, store.number_stars, store.rating, store.size,
                               store.store_network, store.open_hours, store.promotion_days, store.img)
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
        self.data['list_shop_presentation'] = list_temp
        return render(request, 'main/catalog.html', context=self.data)


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


def search(request):
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


class Stor:
    def __init__(self):
        self.id_store = int()
        self.store = None
        self.data = dict()

    def stor(self, request, id_store: int):
        # a = ShopsDataController()
        # a.start()
        self.id_store = id_store
        id_store = Stores.objects.get(id=id_store)
        store = StoreViewItem(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
                              id_store.number_phone, id_store.number_stars, id_store.rating, id_store.size,
                              id_store.store_network, id_store.open_hours, id_store.promotion_days, id_store.img.image)
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
        return render(request, 'main/store.html', context=self.data)


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


def forum(request):
    return render(request, 'main/forum.html')
