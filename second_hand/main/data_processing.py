from .parsers import ModaMaxParser
import re
from datetime import datetime, date, timedelta


class ModaMaxParserDataProcessor:
    def __init__(self):
        self.__list_shops = list()
        self.__modamax_data = dict()

    def get_parsing_results(self):
        self.__modamax_data = ModaMaxParser().dict_shop_data
        for key, value in self.__modamax_data.items():
            dict_schedule = self.get_schedule(value[-1].text)
            dict_many = self.get_descaunt(value[:-1])
            self.__list_shops.append(ShopsData(key, dict_schedule, dict_many))
        return self.__list_shops

    def get_descaunt(self, many_descaunt):
        dict_ = dict()
        for i in range(len(many_descaunt)):
            many = re.search(r'^\S*\s*(\S+)\s*(\d+)\s*(\d+)\s*(.*)\n\ *\s*(.*)\s*', many_descaunt[i].text)
            dict_[many.group(1).capitalize()] = [many.group(2) + '.' + many.group(3), many.group(4), many.group(5)]
        return dict_

    def time(self, start, finish, day_number):
        dat = str(date.today() + timedelta(days=day_number))
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


class ShopsData:
    def __init__(self, address, schedule, many_descaunt):
        self.address = address
        self.dict_schedule = schedule
        self.dict_discounts = many_descaunt

# a = ShopsDataController()
# m = ModaMaxParserDataProcessor()
# list_ModaMax = m.list_shops
# for shop in list_ModaMax:
#     for key, value in shop.dict_discounts.items():
#         print(key, value)
#     for key, value in shop.dict_schedule.items():
#         print(key, value)