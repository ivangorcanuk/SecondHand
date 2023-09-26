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
import requests
import re
from datetime import datetime, date, timedelta
from .forms import SearchForm
from django.db.models import Q

# придумать хитрый механизм для отображения рабочего времени по дням недели!
# добавить уникальность open_hours


def index(request):
    return render(request, 'main/index.html')


class Catalog:

    list_discounts = list()
    base_sale = PromotionsRegister.objects.values_list('general_promotions', flat=True)
    for discount in base_sale:
        if discount is not None and len(discount) > 4 and discount != 'Выходной':
            list_discounts.append(discount)
    list_discounts = list(set(list_discounts))

    data = {
        'list_name_network': ['Мода Макс', 'Эконом Сити', 'Адзенне', 'Мегахенд'],
        'cities': ['Минск'],
        'list_sizes': ['S', 'M', 'L'],
        'sales': ['-30%', '-40%', '-60%', '-80%'],
        'discounts': list_discounts,
        'list_social_discounts': ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%'],
        'search': '',
        'network': '',
        'sale': 'Выберите скидку',
        'discount': 'Выберите акцию',
        'size': '',
        'selected_date': '',
    }

    def __init__(self):
        self.base_shop = Stores.objects.all()
        self.list_shops = self.convert_to_view_item(self.base_shop)
        self.discounts = PromotionsRegister.objects.all()

    def catalog(self, request):
        self.data['list_shop_presentation'] = self.list_shops
        self.data['search'] = ''
        self.data['network'] = ''
        self.data['size'] = ''
        self.data['selected_date'] = ''
        return render(request, 'main/catalog.html', context=self.data)

    def handle_search(self, request):
        if request.GET.get('search') is not None:
            search_str = request.GET.get('search')
            self.data['search'] = search_str
            list_shop_presentation = list()
            for shop in self.list_shops:
                name_store = shop.name_store
                address = shop.address
                if search_str.upper() in name_store.upper() or search_str.upper() in address.upper():
                    list_shop_presentation.append(shop)
            self.data['list_shop_presentation'] = list_shop_presentation
            return render(request, 'main/catalog.html', context=self.data)

    def handle_filtering(self, request):
        list_shops_sorted = self.list_shops
        shops_one_city = request.GET.get('city')
        list_store_network = request.GET.getlist('store_network')
        list_shop_size = request.GET.getlist('shop_size')
        sale = request.GET.get('sales')
        discount = request.GET.get('discount')
        date_to_search = request.GET.get('date')
        week_day = str()

        if list_store_network:  # если заполнен
            list_shops_sorted = self.sort_by_shop_network(list_store_network, list_shops_sorted)

        if list_shop_size:
            list_shops_sorted = self.sort_by_shop_size(list_shop_size, list_shops_sorted)

        if date_to_search:
            week_day = str(date.weekday(date.today()))

        if sale != 'Выберите скидку':
            list_shops_sorted = self.processes_sale(list_shops_sorted, sale, week_day)

        if discount != 'Выберите акцию':
            list_shops_sorted = self.processes_sale(list_shops_sorted, discount, week_day)

        self.data['list_shop_presentation'] = list_shops_sorted
        self.data['network'] = list_store_network
        self.data['sale'] = sale
        self.data['discount'] = discount
        self.data['size'] = list_shop_size
        self.data['selected_date'] = date_to_search

        return render(request, 'main/catalog.html', context=self.data)

    def sort_by_shop_network(self, list_shops_network, list_shops_sorted):
        list_temp = list()
        for shop in list_shops_sorted:
            if shop.name_store in list_shops_network:
                list_temp.append(shop)
        return list_temp

    def sort_by_shop_size(self, list_shop_size, list_shops_sorted):
        list_temp = list()
        for shop in list_shops_sorted:
            if shop.size in list_shop_size:
                list_temp.append(shop)
        return list_temp

    def processes_sale(self, list_shops_sorted, discount, week_day):
        discounts = PromotionsRegister.objects.filter(general_promotions=discount)
        list_temp = list()
        for i in discounts:
            for stor in list_shops_sorted:
                if week_day == '':
                    for j in range(datetime.weekday(date.today()), len(stor.list_promotion)):
                        list_id = stor.list_promotion[j].split('*')
                        if str(i.id) in list_id:
                            list_temp.append(stor)
                else:
                    list_id = stor.list_promotion[int(week_day)].split('*')
                    if str(i.id) in list_id:
                        list_temp.append(stor)
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
                              'Всё по 2 рубля', 'Всё по 4 рубля', 'Всё по 4 рубля']
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
    form = SearchForm()
    date = {
        'form': form
    }
    return render(request, 'main/map.html', context=date)


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
    def stor(self, request, id_store: int):
        # a = ShopsDataController()
        # a.start()

        id_store = Stores.objects.get(id=id_store)
        store = StoreViewItem(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.address,
                              id_store.number_phone, id_store.number_stars, id_store.rating, id_store.size,
                              id_store.store_network, id_store.open_hours, id_store.promotion_days, id_store.img.image)
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
