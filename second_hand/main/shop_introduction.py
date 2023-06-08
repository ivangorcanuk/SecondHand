from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours
from datetime import datetime, date


class Store:
    weekdays = {'1': 'Пн',
                '2': 'Вт',
                '3': 'Ср',
                '4': 'Чт',
                '5': 'Пт',
                '6': 'Сб',
                '7': 'Вс'}

    def __init__(self, id_store, name_store, country, city, area, street, house, floor,
                 number_phone, number_stars, rating, store_network, open_hours):
        self.id = id_store
        self.name_store = name_store
        self.country = country
        self.city = city
        self.area = area
        self.street = street
        self.house = house
        self.floor = floor
        self.number_phone = number_phone
        self.number_stars = number_stars
        self.rating = rating
        self.store_network = store_network
        self.id_open_hours = open_hours
        self.opening_hours_today = self.col()  # готовая строка для отображения рабочего времени
        self.prob = self.cikl()
        #self.list_week_day = self.col()

    def col(self):
        day_week = datetime.weekday(datetime.now())  # вытянули намер дня недели (0,1..)
        # date_current = str(date.today())  # получили сегодняшнюю дату
        # date_current = date_current.replace('-', '.')  # заменяет черточки на точки
        # date_current = str(day_week) + ', ' + date_current  # сформировали строку
        # full_date = datetime.strptime(date_current, "%w, %d.%m.%Y").strftime("%A, %d %B %Y")
        # week_day = full_date[:full_date.find(',')].lower()  # получили день недели
        dict_week = self.week()
        for i in range(len(dict_week)):
            if dict_week[list(dict_week.keys())[i]][2] == day_week + 1:
                day = dict_week[list(dict_week.keys())[i]][1]
                return day[:2] + ':00 - ' + day[2:] + ':00'

    def cikl(self):
        dict_week = self.week()
        is_o = True
        b = int()
        list_ap = list()
        for i in range(6):
            if dict_week[list(dict_week.keys())[i]][1] == dict_week[list(dict_week.keys())[i + 1]][1]:
                if is_o:
                    b = i
                is_o = False
            else:
                time = dict_week[list(dict_week.keys())[b]][1]
                time = time[:2] + ':00 - ' + time[2:] + ':00'
                forma = dict_week[list(dict_week.keys())[b]][0] + '-' + dict_week[list(dict_week.keys())[i]][0] + ': ' + time
                is_o = True
                list_ap.append(forma)
            if len(dict_week) == i + 2:
                time = dict_week[list(dict_week.keys())[b]][1]
                time = time[:2] + ':00 - ' + time[2:] + ':00'
                forma = dict_week[list(dict_week.keys())[b]][0] + '-' + dict_week[list(dict_week.keys())[i]][0] + ': ' + time
                list_ap.append(forma)
                break
        return list_ap

    def week(self):
        monday = self.id_open_hours.monday
        tuesday = self.id_open_hours.tuesday
        wednesday = self.id_open_hours.wednesday
        thursday = self.id_open_hours.thursday
        friday = self.id_open_hours.friday
        saturday = self.id_open_hours.saturday
        sunday = self.id_open_hours.sunday
        return {'monday': ['Пн', monday, 1],
                'tuesday': ['Вт', tuesday, 2],
                'wednesday': ['Ср', wednesday, 3],
                'thursday': ['Чт', thursday, 4],
                'friday': ['Пт', friday, 5],
                'saturday': ['Сб', saturday, 6],
                'sunday': ['Вс', sunday, 7]}

