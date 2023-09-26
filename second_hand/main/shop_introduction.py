from .models import PromotionsRegister, StoreNetwork, Stores, LinkSocNetworks, OpenHours
from datetime import datetime, date


class StoreViewItem:
    list_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    def __init__(self, id_store, name_store, country, city, address, number_phone,
                 number_stars, rating, size, store_network, open_hours, promotion_days, img):
        self.id = id_store
        self.name_store = name_store
        self.country = country
        self.city = city
        self.address = address
        self.number_phone = number_phone
        self.number_stars = number_stars
        self.rating = rating
        self.size = size
        self.store_network = store_network
        self.img = img
        self.list_open_hours = [
                        [open_hours.mon_st, open_hours.mon_fn],
                        [open_hours.tue_st, open_hours.tue_fn],
                        [open_hours.wed_st, open_hours.wed_fn],
                        [open_hours.thu_st, open_hours.thu_fn],
                        [open_hours.fri_st, open_hours.fri_fn],
                        [open_hours.sat_st, open_hours.sat_fn],
                        [open_hours.sun_st, open_hours.sun_fn]
                               ]
        self.list_promotion = [
                        promotion_days.monday,
                        promotion_days.tuesday,
                        promotion_days.wednesday,
                        promotion_days.thursday,
                        promotion_days.friday,
                        promotion_days.saturday,
                        promotion_days.sunday
                               ]
        for day in self.list_open_hours:
            if day[0] is None and day[1] is None:
                temp = datetime(year=2001, month=1, day=1, hour=0, minute=0, second=0)  # временно обозначили выходной
                day[0] = temp
                day[1] = temp

        self.opening_hours_today_text = self.get_todays_open_hours()  # готовая строка для отображения рабочего времени
        self.list_days_open_hours = self.prepare_week_schedule()  # заполнили список днями с рабочим расписанием
        self.list_promotion_days = self.get_promotion_list_by_id()
        self.list_catalog_prom_days = self.list_promotion_days[datetime.weekday(date.today()):len(self.list_promotion_days)]

    def get_todays_open_hours(self):
        for day in self.list_open_hours:
            if date.today() == day[0].date():
                start_str = datetime.strptime(str(day[0].time()), "%H:%M:%S").strftime("%H:%M")
                finish_str = datetime.strptime(str(day[1].time()), "%H:%M:%S").strftime("%H:%M")
                #print(start_str + ' - ' + finish_str)
                return start_str + ' - ' + finish_str
        return 'Выходной'

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
                    (self.list_open_hours[i - 1][1].time() == self.list_open_hours[i][1].time()):  # если вчера и сегодня работа начинается и заканчивается в одно время
                is_new_sequence = False
            elif (self.list_open_hours[i - 1][0].time() != self.list_open_hours[i][0].time() or
                  self.list_open_hours[i - 1][1].time() != self.list_open_hours[i][1].time()) or i == 6:
                if first_day != i - 1:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.list_week[first_day], self.list_week[i - 1])
                else:
                    forma = self.get_time_str(self.list_open_hours[i - 1], self.list_week[first_day])
                list_days_open_hours.append(forma)
                is_new_sequence = True
        if (self.list_open_hours[-1][0].time() != self.list_open_hours[-2][0].time()) or \
                (self.list_open_hours[-1][1].time() != self.list_open_hours[-2][1].time()):
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.list_week[6]))
        else:
            list_days_open_hours.append(self.get_time_str(self.list_open_hours[-1], self.list_week[first_day], self.list_week[6]))

        for i in range(len(list_days_open_hours)):
            list_days_open_hours[i] = list_days_open_hours[i].replace('00:00 - 00:00', 'Выходной')
        # for schedule in list_days_open_hours:
        #     print(schedule)

        return list_days_open_hours

    def get_promotion_list_by_id(self):
        list_temp = list()
        for element in self.list_promotion:  # проходим по списку с id скидок
            list_promotion = list()
            if element == '':
                list_promotion.append('Нет скидки')
            else:
                list_id_promotion = element.split('*')  # разбили склеиный элемент и поместили в отдельный список
                for j in list_id_promotion:
                    promotion = PromotionsRegister.objects.get(id=int(j))
                    list_promotion.append(promotion.promotion_name)
            list_temp.append(tuple(list_promotion))
        # for i in list_temp:
        #     print(i)
        return list_temp