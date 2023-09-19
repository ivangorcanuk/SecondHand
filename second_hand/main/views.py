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


class Catalog:

    list_discounts = list()
    base_sale = PromotionsRegister.objects.values_list('general_promotions', flat=True)
    for discount in base_sale:
        if discount is not None and len(discount) > 4 and discount != 'Выходной':
            list_discounts.append(discount)
    list_discounts = list(set(list_discounts))

    data = {
        'name_network': ['Мода Макс', 'Эконом Сити', 'Адзенне', 'Мегахенд'],
        'cities': ['Минск'],
        'sizes': ['S', 'M', 'L'],
        'sales': ['-20%', '-40%', '-60%', '-80%'],
        'discounts': list_discounts,
        'list_social_discounts': ['Пенсионерам', 'Студентам', 'Детям', 'Семейные', 'На всё от 80%'],
        'this_day': datetime.strftime(date.today(), "%d.%m.%Y"),
        'search': '',
    }

    def catalog(self, request):
        base_shop = Stores.objects.all()
        self.data['list_shop_presentation'] = self.stor(base_shop)
        self.data['search'] = ''
        return render(request, 'main/catalog.html', context=self.data)

    def search(self, request):
        if request.method == 'GET':
            if request.GET.get('search') is not None:
                search = request.GET.get('search')
                self.data['search'] = search
                list_stor = Stores.objects.filter(Q(name_store__icontains=search) | Q(address__icontains=search))
                if list_stor is not None:
                    list_shop_presentation = list()
                    for store in list_stor:
                        st = Store(store.id, store.name_store, store.country, store.city, store.address,
                                   store.number_phone, store.number_stars, store.rating,
                                   store.store_network, store.open_hours, store.promotion_days)
                        list_shop_presentation.append(st)

                    self.data['list_shop_presentation'] = list_shop_presentation

                    return render(request, 'main/catalog.html', context=self.data)
                else:
                    return render(request, 'main/catalog.html', context=self.data)

    def filter(self, request):
        if request.method == 'GET':
            print(request.GET.get('city'))
            print(request.GET.getlist('store_network'))
            print(request.GET.getlist('shop_size'))
            print(request.GET.get('sales'))
            print(request.GET.get('discounts'))
            print(request.GET.get('date'))
            shops_one_city = None
            list_shops = list()
            list_store_network = request.GET.get('store_network')
            if list_store_network:  # если заполнен
                for network in list_store_network:
                    list_temp = Stores.objects.filter(name_store__icontains=network)
                    list_shops += list_temp
                self.data['list_shop_presentation'] = self.stor(list_shops)
                return render(request, 'main/catalog.html', context=self.data)
            else:
                return render(request, 'main/catalog.html', context=self.data)
            # if request.GET.get('city') is not None:  # установить постоянное значение
            #     city = request.GET.get('city')
            #     list_stor = Stores.objects.filter(city__icontains=city)
            # if request.GET.get('store_network') is not None:  # установить постоянное значение
            #     network = request.GET.get('store_network')
            #     list_stor = Stores.objects.filter(name_store__icontains=network)
            # if request.GET.get('shop_size') is not None:  # установить постоянное значение
            #     size = request.GET.get('shop_size')
            #     list_stor = Stores.objects.filter(size__icontains=size)
            # if request.GET.get('sales') is not None:  # установить постоянное значение
            #     sale = request.GET.get('sales')
            #     # искать в структуре класса
            # if request.GET.get('discounts') is not None:  # установить постоянное значение
            #     discount = request.GET.get('discounts')
            #     # искать в структуре класса
            # if request.GET.get('date') is not None:  # установить постоянное значение
            #     date = request.GET.get('date')
                # подумать

    def stor(self, base_shop):
        list_shop_presentation = list()
        for store in base_shop:  # прошлись по таблице с магазинами и отправили данные в класс представления
            st = Store(store.id, store.name_store, store.country, store.city, store.address,
                       store.number_phone, store.number_stars, store.rating,
                       store.store_network, store.open_hours, store.promotion_days)
            list_shop_presentation.append(st)
        return list_shop_presentation



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


class Stor:
    def stor(self, request, id_store: int):
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
