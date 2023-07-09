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

    def __init__(self, id_store, name_store, country, city, address, number_phone,
                 number_stars, rating, store_network, open_hours):
        self.id = id_store
        self.name_store = name_store
        self.country = country
        self.city = city
        self.address = address
        self.number_phone = number_phone
        self.number_stars = number_stars
        self.rating = rating
        self.store_network = store_network
        self.list_open_hours = [
                        (open_hours.mon_st, open_hours.mon_fn),
                        (open_hours.tue_st, open_hours.tue_fn),
                        (open_hours.wed_st, open_hours.wed_fn),
                        (open_hours.thu_st, open_hours.thu_fn),
                        (open_hours.fri_st, open_hours.fri_fn),
                        (open_hours.sat_st, open_hours.sat_fn),
                        (open_hours.sun_st, open_hours.sun_fn)
        ]
        #self.list_promotion_days = list_promotion_days
        self.opening_hours_today_text = self.get_todays_open_hours()  # готовая строка для отображения рабочего времени
        #self.discount_today = list_promotion_days[datetime.weekday(datetime.now())]
        self.list_days_open_hours = self.prepare_week_schedule()  # заполнили список днями с рабочим расписанием

    def get_todays_open_hours(self):
        for day in self.list_open_hours:
            if date.today() == day[0].date():
                start_str = datetime.strptime(str(day[0].time()), "%H:%M:%S").strftime("%H:%M")
                finish_str = datetime.strptime(str(day[1].time()), "%H:%M:%S").strftime("%H:%M")
                return start_str + ' - ' + finish_str

    def get_time_str(self, day, first_day=str(), second_day=str()):
        start_str = datetime.strptime(str(day[0].time()), "%H:%M:%S").strftime("%H:%M")
        finish_str = datetime.strptime(str(day[1].time()), "%H:%M:%S").strftime("%H:%M")
        time_str = start_str + ' - ' + finish_str
        if first_day != str() and second_day == str():
            forma = first_day + ': ' + time_str
        elif first_day != str() and second_day != str():
            forma = first_day + '-' + second_day + ': ' + time_str
        else:
            return None
        return forma

    def prepare_week_schedule(self):  # формирует список с готовыми строками для отображения пользователям
        is_new_sequence = True  # это новая последовательность? (да/нет)
        first_day = int()
        list_days_open_hours = list()
        for i in range(1, 7):
            if is_new_sequence:
                first_day = i - 1
            if (self.list_open_hours[i - 1][0].time() == self.list_open_hours[i][0].time()) and \
                    (self.list_open_hours[i - 1][1].time() == self.list_open_hours[i][1].time()):
                is_new_sequence = False
            elif (self.list_open_hours[i - 1][0].time() != self.list_open_hours[i][0].time() or
                  self.list_open_hours[i - 1][1].time() != self.list_open_hours[i][1].time()) or i == 6:
                if first_day != i - 1:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.dict_weekdays[first_day], self.dict_weekdays[i - 1])
                else:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.dict_weekdays[first_day])
                list_days_open_hours.append(forma)
                is_new_sequence = True
        if (self.list_open_hours[-1][0].time() != self.list_open_hours[-2][0].time()) or \
                (self.list_open_hours[-1][1].time() != self.list_open_hours[-2][1].time()):
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.dict_weekdays[6]))
        else:
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.dict_weekdays[first_day], self.dict_weekdays[6]))
        return list_days_open_hours

