from .parsers import ModaMaxParser, EconomCityParser
import re
from datetime import datetime, date, timedelta


class ModaMaxParserDataProcessor:
    def __init__(self):
        self.__list_shops = list()
        self.__modamax_data = dict()

    def get_parsing_results(self):
        self.__modamax_data = ModaMaxParser().get_data()
        for key, value in self.__modamax_data.items():
            dict_schedule = self.get_schedule(value[-1].text)
            dict_discount = self.get_discount(value[:-1])
            self.__list_shops.append(ShopsData(key, dict_schedule, dict_discount))
        # for value in self.__list_shops:
        #     print(value.address)
        return self.__list_shops

    def get_discount(self, many_descaunt):
        dict_ = dict()
        for i in range(len(many_descaunt)):
            many = re.search(r'^\S*\s*(\S+)\s*(\d+)\s*(\d+)\s*(.*)\n\ *\s*(.*)\s*', many_descaunt[i].text)
            dict_[many.group(1).capitalize()] = [many.group(2) + '.' + many.group(3), many.group(4), many.group(5)]
        return dict_

    def time(self, start, finish, day_number):
        monday = date.today() - timedelta(days=date.weekday(date.today()))  # вернули понедельник
        dat = str(monday + timedelta(days=day_number))
        str_datetime_start = dat + ' ' + start
        str_datetime_finsh = dat + ' ' + finish
        date_time_start = datetime.strptime(str_datetime_start, '%Y-%m-%d %H:%M')
        date_time_finsh = datetime.strptime(str_datetime_finsh, '%Y-%m-%d %H:%M')
        return [date_time_start, date_time_finsh]

    def get_schedule(self, schedule):
        dict_week = {
            'Пн': [],
            'Вт': [],
            'Ср': [],
            'Чт': [],
            'Пт': [],
            'Сб': [],
            'Вс': [],
        }
        days = str()
        i = 0
        if '.' in schedule:
            schedule = schedule.replace('.', ':')

        for key, value in dict_week.items():
            start_finish = re.search(r'(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', schedule)  # вытянули первое вхождение начала и конца рабочего дня
            if re.search(f'{key}', schedule):  # если в строке есть день недели
                days = re.search(f'{key}\S*:', schedule)  # вытянули его days
                start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', schedule)  # воспользовались days как ориентиром, чтобы отыскать его время работы .\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)
                value += self.time(start_finish.group(1), start_finish.group(2), i)
            else:
                if days != None and days.group(0)[2] == '-':
                    start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', schedule)
                    value += self.time(start_finish.group(1), start_finish.group(2), i)
                else:
                    value += self.time(start_finish.group(1), start_finish.group(2), i)
            i += 1

        return dict_week


class EconomCityParserDataProcessor:
    list_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    def __init__(self):
        self.__list_shops = list()
        self.__economcity_data = dict()
        self.__exception_full_change = str()  # исключение работы магазина в день полной смены товара
        self.__exception_all_by_3 = str()  # исключение работы магазина в день акции все по 3 рубля

    def get_parsing_results(self):
        self.__economcity_data = EconomCityParser().get_data()
        for key, value in self.__economcity_data.items():
            dict_schedule = self.get_schedule(value[-1].text)
            dict_discounts = self.get_discount(value[:-1])
            if self.__exception_full_change:
                dict_schedule = self.update_special_day(dict_schedule, dict_discounts)
            # self.__list_shops.append(ShopsData(key, dict_schedule, dict_discounts))
            print(key)
            for key, value in dict_schedule.items():
                print(key, value)
            for key, value in dict_discounts.items():
                print(key, value)
        return self.__list_shops

    def get_discount(self, list_discounts):
        dict_discounts = dict()
        day_of_week = date.weekday(date.today())
        # "temp_.." - времен. переменная "cur" - текущая переменная
        ind = 0
        for i in range(len(list_discounts)):
            if 'Cегодня' in list_discounts[i].text:
                for j in range(i - day_of_week, i - day_of_week + 7):
                    data_discount = re.search(r'\n(.+)\n+\s*(.*)\n\s*(.*)\n*$', list_discounts[j].text)
                    dict_discounts[self.list_week[ind]] = [data_discount.group(2), data_discount.group(3)]
                    ind += 1
        return dict_discounts

    def convert_to_datetime(self, start, finish, day_number):
        monday = date.today() - timedelta(days=date.weekday(date.today()))  # вернули понедельник
        dat = str(monday + timedelta(days=day_number))
        str_datetime_start = dat + ' ' + start
        str_datetime_finsh = dat + ' ' + finish
        date_time_start = datetime.strptime(str_datetime_start, '%Y-%m-%d %H:%M')
        date_time_finsh = datetime.strptime(str_datetime_finsh, '%Y-%m-%d %H:%M')
        return [date_time_start, date_time_finsh]

    def get_schedule(self, schedule_raw):
        dict_schedule = {
            'Пн': [],
            'Вт': [],
            'Ср': [],
            'Чт': [],
            'Пт': [],
            'Сб': [],
            'Вс': [],
        }
        without_enter_schedule = schedule_raw.replace('\n', '')
        converted_timetable = re.search(r'(.+)В день полной', without_enter_schedule)
        converted_timetable = converted_timetable.group(1).replace('.', ':')
        self.__exception_full_change = re.search(r'В день полной\D*(\d*.\d*\s*.\s*\d*.\d*)', without_enter_schedule)
        if re.search(r'В день акции', without_enter_schedule):
            self.__exception_all_by_3 = re.search(r'В день акции.*(\d\d.\d\d\s*.\s*\d\d.\d\d)', without_enter_schedule)

        days = str()
        i = 0

        for key, value in dict_schedule.items():
            start_finish = re.search(r'(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', converted_timetable)  # вытянули первое вхождение начала и конца рабочего дня
            if re.search(f'{key}', converted_timetable):  # если в строке есть день недели
                days = re.search(f'{key}\S*:', converted_timetable)  # вытянули его days
                start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', converted_timetable)  # воспользовались days как ориентиром, чтобы отыскать его время работы .\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)
                value += self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
            else:
                if days != None and days.group(0)[2] == '-':
                    start_finish = re.search(f'{days.group(0)}.\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', converted_timetable)
                    value += self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
                else:
                    value += self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
            i += 1

        return dict_schedule

    def update_special_day(self, dict_schedule, dict_discounts):
        start_finish = re.search(r'(\S+)\s+.\s+(\S+)', self.__exception_full_change.group(1))
        i = 0  # счетчик дней, до 'Полной смены товара'
        for key, value in dict_discounts.items():
            for j in value:
                if re.search(r'Полная смена товара', j):
                    dict_schedule[key] = self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
                if self.__exception_all_by_3:
                    if re.search(r'Всё по 3 рубля', j):
                        dict_schedule[key] = self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
            i += 1

        return dict_schedule


class ShopsData:
    def __init__(self, address, schedule, dict_discounts):
        self.address = address
        self.dict_schedule = schedule
        self.dict_discounts = dict_discounts