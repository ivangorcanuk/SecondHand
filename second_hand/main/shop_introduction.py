from .models import StoreNetwork, Stores, LinkSocNetworks, OpenHours
from datetime import datetime, date


class Store:
    dict_weekdays = {0: 'Пн',
                     1: 'Вт',
                     2: 'Ср',
                     3: 'Чт',
                     4: 'Пт',
                     5: 'Сб',
                     6: 'Вс'}

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
        self.list_open_hours = [open_hours.monday, open_hours.tuesday, open_hours.wednesday,
                                open_hours.thursday, open_hours.friday, open_hours.saturday,
                                open_hours.sunday]
        self.opening_hours_today_text = self.get_day_of_week()  # готовая строка для отображения рабочего времени
        self.list_days_open_hours = self.prepare_week_schedule()  # заполнили список днями с рабочим расписанием

    def get_day_of_week(self, p_week_day=-1):
        week_day = p_week_day
        if p_week_day == -1:
            week_day = datetime.weekday(datetime.now())  # вытянули намер дня недели (0,1..)
        work_time_value = self.list_open_hours[week_day]
        return work_time_value[:2] + ':00 - ' + work_time_value[2:] + ':00'

    def prepare_week_schedule(self):
        is_new_sequence = True  # это новая последовательность? (да/нет)
        first_day = int()
        list_days_open_hours = list()
        for i in range(6):
            if self.list_open_hours[i] == self.list_open_hours[i+1]:
                if is_new_sequence:
                    first_day = i
                is_new_sequence = False
            else:
                time = self.list_open_hours[i]
                time = time[:2] + ':00 - ' + time[2:] + ':00'
                forma = self.dict_weekdays[first_day] + '-' + self.dict_weekdays[i] + ': ' + time
                is_new_sequence = True
                list_days_open_hours.append(forma)
            if len(self.list_open_hours) == i + 2:
                time = self.list_open_hours[i]
                time = time[:2] + ':00 - ' + time[2:] + ':00'
                forma = self.dict_weekdays[first_day] + '-' + self.dict_weekdays[i] + ': ' + time
                list_days_open_hours.append(forma)
                break
        return list_days_open_hours

# пн-вт  10:00-20:00
# ср-чт  10:00-20:00
# пт-сб  10:00-20:00
# вс     10:00-20:00

