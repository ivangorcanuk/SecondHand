# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours
from .shop_introduction import Store
from django.views.generic import ListView
from datetime import datetime

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
            st = Store(store.id, store.name_store, store.country, store.city, store.area, store.street, store.house, store.floor,
                 store.number_phone, store.number_stars, store.rating, store.store_network, store.open_hours)
            list_shop_presentation.append(st)
            wek = store.city
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
    id_store = Stores.objects.get(id=id_store)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.area, id_store.street,
                  id_store.house, id_store.floor, id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours)
    import datetime
    week_number = datetime.datetime.today().isocalendar()[1]  # получили № недели
    # print(stor.open_hours.week_number)
    # list_days_week = list()
    # for day in week:
    #     if type(day) == str():
    #         list_days_week.append(day)
    # print(list_days_week)
    data = {
        'store': store,
        'week_number': week_number
    }
    return render(request, 'main/store.html', context=data)


def search(request):
    return render(request, 'main/search.html')


def login(request):
    return render(request, 'main/login.html')


def register(request):
    return render(request, 'main/register.html')
