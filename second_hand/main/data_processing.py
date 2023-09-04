from .parsers import ModaMaxParser, EconomCityParser, AdzenneParser, MegahandParser
import re
from datetime import datetime, date, timedelta


class Data:
    list_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    def __int__(self):
        self.list_shops = list()
        #self.dict_raw_data_shops = dict()

    def convert_to_datetime(self, start, finish, day_number):
        monday = date.today() - timedelta(days=date.weekday(date.today()))  # вернули понедельник
        dat = str(monday + timedelta(days=day_number))
        str_datetime_start = dat + ' ' + start
        str_datetime_finsh = dat + ' ' + finish
        date_time_start = datetime.strptime(str_datetime_start, '%Y-%m-%d %H:%M')
        date_time_finsh = datetime.strptime(str_datetime_finsh, '%Y-%m-%d %H:%M')
        return [date_time_start, date_time_finsh]

    def conv(self, day_number, converted_timetable, dict_schedule, days=''):
        start_finish = re.search(f'{days}.\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)', converted_timetable)  # воспользовались days как ориентиром, чтобы отыскать его время работы .\s*(\d*\d.\d\d*)\D+(\d*\d.\d\d*)
        dict_schedule[self.list_week[day_number]] = self.convert_to_datetime(start_finish.group(1), start_finish.group(2), day_number)
        return dict_schedule

    def get_schedule(self, converted_timetable):
        converted_timetable = converted_timetable.replace('.', ':')
        day = str()
        dict_schedule = dict()

        for i in range(7):
            if self.list_week[i] in converted_timetable:  # если в строке есть день недели
                day = re.search(f'{self.list_week[i]}\S*:', converted_timetable)  # вытянули его days
                day = day.group(0)
                dict_schedule = self.conv(i, converted_timetable, dict_schedule, day)
            else:
                if day != '':
                    if day[2] == '-':
                        dict_schedule = self.conv(i, converted_timetable, dict_schedule, day)
                    else:
                        dict_schedule = self.conv(i, converted_timetable, dict_schedule)
                else:
                    dict_schedule[self.list_week[i]] = None

        return dict_schedule


class ModaMaxParserDataProcessor(Data):
    def __init__(self):
        #Data.__init__(self)
        self.__list_shops = list()
        self.__modamax_data = dict()

    def get_parsing_results(self):
        self.__modamax_data = ModaMaxParser().get_data()
        for key, value in self.__modamax_data.items():
            dict_schedule = Data.get_schedule(self, value[-1].text)
            dict_discounts = self.get_discount(value[:-1])
            self.__list_shops.append(ShopsData(key, dict_schedule, dict_discounts))
            print(key)
            for key, value in dict_schedule.items():
                print(key, value)
            for key, value in dict_discounts.items():
                print(key, value)
        print('ASD')
        return self.__list_shops

    def get_discount(self, many_descaunt):
        dict_ = dict()
        for i in range(len(many_descaunt)):
            many = re.search(r'^\S*\s*(\S+)\s*(\d+)\s*(\d+)\s*(.*)\n\ *\s*(.*)\s*', many_descaunt[i].text)
            dict_[many.group(1).capitalize()] = [many.group(2) + '.' + many.group(3), many.group(4), many.group(5)]
        return dict_


class EconomCityParserDataProcessor(Data):
    list_discount = ['День сеньора', '3я вещь в подарок', 'Большое пополнение', '-20%', '-30%', '-40%', '-50%', '-60%',
                     'Всё по 3 рубля', 'Полна смена товара', 'обувь + текстиль', 'Детский день', 'Текстиль',
                     'Товар премиум', 'x2 скидка по дисконту', '4я вещь в подарок', 'Пополнение товара', '-80%',
                     'Большое поступление', 'винтаж', 'Обувь+текстиль', '-70%']

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
                dict_schedule = self.update_special_day(dict_schedule, dict_discounts, self.__exception_full_change)
            if self.__exception_all_by_3:
                dict_schedule = self.update_special_day(dict_schedule, dict_discounts, self.__exception_all_by_3)
            self.__list_shops.append(ShopsData(key, dict_schedule, dict_discounts))
            print(key)
            for key, value in dict_schedule.items():
                print(key, value)
            for key, value in dict_discounts.items():
                print(key, value)
        return self.__list_shops

    def get_discount(self, list_discounts):
        dict_discounts = dict()
        day_of_week = date.weekday(date.today())  # хранит сегоднешний день в цифре 0..6
        # "temp_.." - времен. переменная "cur" - текущая переменная
        ind = 0

        for i in range(len(list_discounts)):
            if 'Cегодня' in list_discounts[i].text:
                for j in range(i - day_of_week, i - day_of_week + 7):
                    data_discount = re.search(r'\n(.+)\n+\s*(.*)\n\s*(.*)\n*$', list_discounts[j].text)
                    dict_discounts[self.list_week[ind]] = [data_discount.group(2), data_discount.group(3)]
                    ind += 1

        for key, value in dict_discounts.items():
            list_temp = []
            for discount in value:
                for i in self.list_discount:
                    if i in discount:
                        list_temp.append(i)
            if not len(list_temp):
                list_temp.append('')
            dict_discounts[key] = list_temp

        return dict_discounts

    def get_schedule(self, schedule_raw):

        without_enter_schedule = re.search(r'(.*\n*.+)\nВ день полной', schedule_raw)
        without_enter_schedule = without_enter_schedule.group(1).replace('\r', '')
        without_enter_schedule = without_enter_schedule.split('\n')
        without_enter_schedule = without_enter_schedule[0] + without_enter_schedule[1]
        converted_timetable = without_enter_schedule.replace(' :', ':')
        if 'В день полной' in schedule_raw:
            temp_time_full_change = re.search(r'В день полной\D*(\d*.\d*\s*.\s*\d*.\d*)', schedule_raw)
            self.__exception_full_change = temp_time_full_change.group(1)

        if 'В день акции' in schedule_raw:
            temp_time_all_by_3 = re.search(r'В день акции.*(\d\d.\d\d\s*.\s*\d\d.\d\d)', schedule_raw)
            self.__exception_all_by_3 = temp_time_all_by_3.group(1)

        return Data.get_schedule(self, converted_timetable)

    def update_special_day(self, dict_schedule, dict_discounts, str_work_hours):
        start_finish = re.search(r'(\S+)\s+.\s+(\S+)', str_work_hours)
        i = 0  # счетчик дней, до 'Полной смены товара'
        for key, value in dict_discounts.items():
            for j in value:
                if 'Полная смена товара' in j:
                    dict_schedule[key] = self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
                if 'Всё по 3 рубля' in j:
                    dict_schedule[key] = self.convert_to_datetime(start_finish.group(1), start_finish.group(2), i)
            i += 1

        return dict_schedule


class AdzenneParserDataProcessor(Data):
    list_week_bel = ['пн', 'аў', 'ср', 'чц', 'пт', 'сб', 'ндз']
    list_streets = [
        ('Крама па вул. Бурдзейнага, 8', 'ул. Бурдейного, 8'),
        ('Крама па вул. В. Харужай, 18/1', 'ул. Веры Хоружей, 18/1'),
        ('Крама па пр. Газеты Праўда, 17', 'пр. Газеты Правда, 17'),
        ('Крама па вул. Громава, 28', 'ул. Громова, 28'),
        ('Крама па пр. Жукава, 25/1', 'пр. Жукова, 25/1'),
        ('Крама па вул. Кіжаватава, 66', 'ул. Лейтенанта Кижеватова, 66'),
        ('Крама па вул. Матусевіча, 68', 'ул. Матусевича, 68'),
        ('Крама па вул. Маякоўскага, 16', 'ул. Маяковского, 16'),
        ('Крама па пр. Незалежнасці, 155/1', 'пр. Независимости, 155/1'),
        ('Крама па пр. Партызанскiм, 56/2', 'пр. Партизанский, 56/2'),
        ('Крама па вул. Платонава, 34', 'ул. Платонова, 34'),
        ('Крама па пр. Ракасоўскага, 150б', 'пр. Рокоссовского, 150б'),
        ('Крама па вул. Русіянава, 7', 'ул. Руссиянова, 7'),
        ('Крама па вул. Сярова, 3а', 'ул. Серова, 3а'),
        ('Крама па вул. Л. Бяды, 39', 'ул. Леонида Беды, 39'),
        ('Крама па вул. В. Харужай, 8', 'ул. Веры Хоружей, 8')
                    ]

    def __init__(self):
        self.__list_shops = list()
        self.__adzenne_data = dict()

    def get_parsing_results(self):
        self.__adzenne_data = AdzenneParser().get_data()
        for key, value in self.__adzenne_data.items():
            street = self.translate_street_bel(key)
            dict_schedule = self.schedule(street, value[-1])
            dict_discounts = self.get_discount(value[:-1])
            dict_schedule = self.update_special_day(dict_discounts, dict_schedule)
            self.__list_shops.append(ShopsData(street, dict_schedule, dict_discounts))
            print(street)
            for key, value in dict_schedule.items():
                print(key, value)
            for key, value in dict_discounts.items():
                print(key, value)
        return self.__list_shops

    def translate_street_bel(self, street_by):
        for i in range(len(self.list_streets)):
            if street_by in self.list_streets[i]:
                return self.list_streets[i][1]

    def get_discount(self, list_discounts):
        dict_discounts = dict()
        day_of_week = date.weekday(date.today())  # хранит сегоднешний день в цифре 0..6
        monday = date.today() - timedelta(day_of_week)  # вернули понедельник
        monday = str(monday.day)
        if monday[0] == '0':  # если день начинается с 0 убираем этот 0
            monday = monday[1]

        ind = 0
        is_cur_week = False

        for raw_day in list_discounts:  # в пустых ячейках с днями проставили ' '
            if raw_day.text == '':
                raw_day = ' '

        for raw_day in list_discounts:
            data_discount = re.search(r'\n*(\d*)\n*\S*\s*(.*)\n*', raw_day.text)
            if monday == data_discount.group(1):
                is_cur_week = True

            if is_cur_week:
                dict_discounts[self.list_week[ind]] = [data_discount.group(2)]
                ind += 1

            if ind == 7:
                break
        return dict_discounts

    def translate_from_bel(self, schedule_by):
        schedule_ru = schedule_by.lower()
        for i in range(len(self.list_week_bel)):
            if self.list_week_bel[i] in schedule_ru:
                schedule_ru = schedule_ru.replace(self.list_week_bel[i], self.list_week[i])
        return schedule_ru

    def schedule(self, street, schedule_raw):
        converted_timetable = schedule_raw.replace('\n', '')
        converted_timetable = converted_timetable.replace('\xa0', ': ')
        if street == 'ул. Веры Хоружей, 8':
            converted_timetable = re.search(r'.*\d', converted_timetable)
            converted_timetable = converted_timetable.group(0)
        converted_timetable = self.translate_from_bel(converted_timetable)

        return Data.get_schedule(self, converted_timetable)

    def update_special_day(self, dict_discounts, dict_schedule):
        i = 0  # счетчик дней, до 'Полной смены товара'
        for key, value in dict_discounts.items():
            if '/Х' in value[0]:
                finish = re.search(r'\d*', value[0])
                finish = finish.group(0) + ':' + '00'
                monday = date.today() - timedelta(days=date.weekday(date.today()))  # вернули понедельник
                dat = str(monday + timedelta(days=i))
                str_datetime_finsh = dat + ' ' + finish
                date_time_finsh = datetime.strptime(str_datetime_finsh, '%Y-%m-%d %H:%M')
                dict_schedule[key][1] = [date_time_finsh]  # изменили время конца рабочего дня
                continue
            if ':)' in value[0] or 'Х' in value[0]:
                dict_schedule[key] = ['Выходной']
            i += 1

        return dict_schedule


class MegahandParserDataProcessor(Data):  # MegahandParser
    list_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    list_address = [
        ('Брикета', 'ул. Брикета, 2'),
        ('Лобанка', 'ул. Лобанка, 94, ТЦ "Maximus"'),
        ('Сурганова', 'ул. Сурганова, 57A, ТЦ "Европа"'),
        ('Дунина-Марцинкевича', 'ул. Дунина-Марцинкевича, 11, ТЦ Раковский Кирмаш')
                   ]

    def __init__(self):
        self.__list_shops = list()
        self.__megahand_data = dict()
        self.__exception_shares_90 = str()  # исключение работы магазина в день акции 90%

    def get_parsing_results(self):
        self.__megahand_data = MegahandParser().get_data()
        for key, value in self.__megahand_data.items():
            address = self.get_address(key)
            dict_schedule = self.get_schedule(value[-1].text)
            dict_discounts = self.get_discount(value[:-1])
            if self.__exception_shares_90:
                dict_schedule = self.update_special_day(dict_schedule, dict_discounts, self.__exception_shares_90)
            self.__list_shops.append(ShopsData(key, dict_schedule, dict_discounts))
            print(f'<<{address}>>')
            for key, value in dict_schedule.items():
                print(key, value)
            for key, value in dict_discounts.items():
                print(key, value)
        return self.__list_shops

    def get_address(self, address):
        for i in self.list_address:
            if i[0] in address:
                return i[1]

    def get_discount(self, list_discounts):
        date_time_obj = None
        day_of_week = date.weekday(date.today())  # хранит сегоднешний день в цифре 0..6
        monday = date.today() - timedelta(day_of_week)  # вернули понедельник
        is_cur_week = False
        day_number = 0
        dict_discounts = dict()
        for i in list_discounts:
            for key, value in i.items():
                if key == 'date':
                    date_time_obj = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                if monday == date_time_obj.date() or is_cur_week:
                    is_cur_week = True
                    if key == 'class':
                        dict_discounts[self.list_week[day_number]] = [value.strip()]
                    if key == 'skidka':
                        dict_discounts[self.list_week[day_number]] += [value]
            if is_cur_week:
                day_number += 1
            if day_number == 7:
                break
        return dict_discounts

    def get_schedule(self, schedule_raw):
        start_finish_time = None
        if 'Ежедневно' in schedule_raw:
            start_finish_time = re.search(r'Ежедневно с\s*(\d\d.\d\d).*(\d\d.\d\d)', schedule_raw)
        if 'В день 90% скидки' in schedule_raw:
            temp_exception_shares_90 = re.search(r'В день 90% скидки с\s*(\d\d.\d\d.*\d\d.\d\d)', schedule_raw)
            self.__exception_shares_90 = temp_exception_shares_90.group(1)

        dict_schedule = dict()

        for i in range(7):
            dict_schedule[self.list_week[i]] = Data.convert_to_datetime(self, start_finish_time.group(1), start_finish_time.group(2), i)

        return dict_schedule

    def update_special_day(self, dict_schedule, dict_discounts, str_work_hours):
        start_finish = re.search(r'(\S+)\s+.*\s+(\S+)', str_work_hours)
        day_counter = 0  # счетчик дней, до 'Полной смены товара'
        for key, value in dict_discounts.items():
            for j in value:
                if '90%' in j:
                    dict_schedule[key] = Data.convert_to_datetime(self, start_finish.group(1), start_finish.group(2), day_counter)
            day_counter += 1

        return dict_schedule


class ShopsData:
    def __init__(self, address, schedule, dict_discounts):
        self.address = address
        self.dict_schedule = schedule
        self.dict_discounts = dict_discounts