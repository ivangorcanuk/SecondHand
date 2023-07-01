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
            st = Store(store.id, store.name_store, store.country, store.city, store.area, store.street,
                       store.house, store.floor, store.number_phone, store.number_stars, store.rating,
                       store.store_network, store.open_hours, store.promotion_days.promotion_days.all())
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
    # def time(s: str):
    #     return datetime.strptime(s, '%Y-%m-%d %H:%M')
    #
    # dict_week = {
    #     'Пн': [],
    #     'Вт': [],
    #     'Ср': [],
    #     'Чт': [],
    #     'Пт': [],
    #     'Сб': [],
    #     'Вс': [],
    # }
    # day_week = 'Пн-сб: 10:00 - 20:00Чт: 9:00 - 20:00Вс: 10:00 - 19:00'
    #
    # days = str()
    # i = 0
    # for key, value in dict_week.items():
    #     start_finish = re.search(r'(\d*\d.\d\d*)\s*\S\s*(\d*\d.\d\d*)',
    #                              day_week)  # вытянули первое вхождение начала и конца рабочего дня
    #     dat = str(date.today() + timedelta(days=i))  # формируем дату
    #     if re.search(f'{key}', day_week):  # если в строке есть день недели
    #         days = re.search(f'{key}\D*:', day_week)  # вытянули его days
    #         start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\s*\S\s*(\d*\d.\d\d*)',
    #                                  day_week)  # воспользовались days как ориентиром, чтобы отыскать его время работы
    #         start_datetime = dat + ' ' + start_finish.group(1)
    #         finsh_datetime = dat + ' ' + start_finish.group(2)
    #         value += [time(start_datetime), time(finsh_datetime)]
    #     else:
    #         if days != None and days.group(0)[2] == '-':
    #             start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\s*\S\s*(\d*\d.\d\d*)', day_week)
    #             start_datetime = dat + ' ' + start_finish.group(1)
    #             finsh_datetime = dat + ' ' + start_finish.group(2)
    #             value += [time(start_datetime), time(finsh_datetime)]
    #         else:
    #             start_datetime = dat + ' ' + start_finish.group(1)
    #             finsh_datetime = dat + ' ' + start_finish.group(2)
    #             value += [time(start_datetime), time(finsh_datetime)]
    #     i += 1
    #
    # for key, value in dict_week.items():
    #     print(key, value)
    #
    # OpenHours(mon_st=dict_week['Пн'][0], mon_fn=dict_week['Пн'][1],
    #           tue_st=dict_week['Вт'][0], tue_fn=dict_week['Вт'][1],
    #           wed_st=dict_week['Ср'][0], wed_fn=dict_week['Ср'][1],
    #           thu_st=dict_week['Чт'][0], thu_fn=dict_week['Чт'][1],
    #           fri_st=dict_week['Пт'][0], fri_fn=dict_week['Пт'][1],
    #           sat_st=dict_week['Сб'][0], sat_fn=dict_week['Сб'][1],
    #           sun_st=dict_week['Вс'][0], sun_fn=dict_week['Вс'][1]).save()

    id_store = Stores.objects.get(id=id_store)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.area, id_store.street,
                  id_store.house, id_store.floor, id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours, id_store.promotion_days.promotion_days.all())
    data = {
        'store': store,
    }
    return render(request, 'main/store.html', context=data)


def search(request):
    id_store = Stores.objects.get(id=3)
    store = Store(id_store.id, id_store.name_store, id_store.country, id_store.city, id_store.area, id_store.street,
                  id_store.house, id_store.floor, id_store.number_phone, id_store.number_stars, id_store.rating,
                  id_store.store_network, id_store.open_hours, id_store.promotion_days.promotion_days.all())
    data = {
        'store': store,
    }
    return render(request, 'main/search.html', context=data)


def login(request):
    return render(request, 'main/login.html')


def register(request):
    return render(request, 'main/register.html')
