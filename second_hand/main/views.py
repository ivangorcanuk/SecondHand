# ListView отображения всего списка
# DetailView детального отображения
# FormView отображения формы
# CreatelView создать запись
# UpdateView изменить запись
# DeleteView удалить запись
from django.shortcuts import render
from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours
from django.views.generic import ListView
from datetime import datetime

# придумать хитрый механизм для отображения рабочего времени по дням недели!
# добавить уникальность open_hours
class Index(ListView):
    template_name = 'main/index.html'
    model = Stores

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        week = self.week()
        print(week)
        #print(self.model.open_hours)
        context['week'] = week
        return context

    def week(self):
        cur = datetime.now()
        day_week = datetime.isoweekday(cur)
        if day_week == 1:
            return 'monday'
        elif day_week == 2:
            return 'tuesday'
        elif day_week == 3:
            return 'wednesday'
        elif day_week == 4:
            return 'thursday'
        elif day_week == 5:
            return 'friday'
        elif day_week == 6:
            return 'saturday'
        elif day_week == 7:
            return 'sunday'


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
    stor = Stores.objects.get(id=id_store)
    week = OpenHours.objects.get(id=str(stor.open_hours))
    import datetime
    week_number = datetime.datetime.today().isocalendar()[1]  # получили № недели
    # print(stor.open_hours.week_number)
    # list_days_week = list()
    # for day in week:
    #     if type(day) == str():
    #         list_days_week.append(day)
    # print(list_days_week)
    data = {
        'store': stor,
        'week_number': week_number
    }
    return render(request, 'main/store.html', context=data)


def search(request):
    return render(request, 'main/search.html')


def login(request):
    return render(request, 'main/login.html')


def register(request):
    return render(request, 'main/register.html')
