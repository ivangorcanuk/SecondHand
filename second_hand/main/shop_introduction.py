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
                 number_phone, number_stars, rating, store_network, open_hours, list_promotion_days):
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
        self.list_open_hours = [open_hours.mon_st, open_hours.mon_fn,
                                open_hours.tue_st, open_hours.tue_fn,
                                open_hours.wed_st, open_hours.wed_fn,
                                open_hours.thu_st, open_hours.thu_fn,
                                open_hours.fri_st, open_hours.fri_fn,
                                open_hours.sat_st, open_hours.sat_fn,
                                open_hours.sun_st, open_hours.sun_fn]
        self.list_promotion_days = list_promotion_days
        self.opening_hours_today_text = self.get_day_of_week()  # готовая строка для отображения рабочего времени
        self.discount_today = list_promotion_days[datetime.weekday(datetime.now())]
        #self.list_days_open_hours = self.prepare_week_schedule()  # заполнили список днями с рабочим расписанием

    def get_day_of_week(self):
        for i in range(len(self.list_open_hours)):
            if date.today() == self.list_open_hours[0].date():
                start_time = self.list_open_hours[i].time().replace(second=0)
                finish_time = self.list_open_hours[i+1].time().replace(second=0)
                start_str = datetime.strptime(str(start_time), "%H:%M:%S").strftime("%H:%M")
                finish_str = datetime.strptime(str(finish_time), "%H:%M:%S").strftime("%H:%M")
                return start_str + ' - ' + finish_str

    def get_time_str(self, time, first_day=str(), second_day=str()):
        time = time[:2] + ':00 - ' + time[2:] + ':00'
        if first_day != str() and second_day == str():
            forma = first_day + ': ' + time
        elif first_day != str() and second_day != str():
            forma = first_day + '-' + second_day + ': ' + time
        else:
            return None
        return forma

    def prepare_week_schedule(self):  # формирует список с готовыми сторакми для отображения пользователям
        is_new_sequence = True  # это новая последовательность? (да/нет)
        first_day = int()
        list_days_open_hours = list()
        for i in range(1, 7):
            if is_new_sequence:
                first_day = i - 1
            if self.list_open_hours[i - 1] == self.list_open_hours[i]:
                is_new_sequence = False
            elif self.list_open_hours[i - 1] != self.list_open_hours[i] or i == 6:
                if first_day != i - 1:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.dict_weekdays[first_day], self.dict_weekdays[i - 1])
                else:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.dict_weekdays[first_day])
                list_days_open_hours.append(forma)
                is_new_sequence = True
        if self.list_open_hours[-1] != self.list_open_hours[-2]:
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.dict_weekdays[6]))
        else:
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.dict_weekdays[first_day], self.dict_weekdays[6]))
        return list_days_open_hours

