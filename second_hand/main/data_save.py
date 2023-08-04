from .models import Stores, PromotionsRegister, OpenHours, PromotionDays


class ShopsDataDBSaver:
    def __int__(self):
        self.__list_stores = Stores.objects.all()
        self.__list_discounts = PromotionsRegister.objects.all()

    def save_datetime_work(self, address, dict_schedule):
        is_not_found = True
        for shop in self.__list_stores:
            if shop.address == address:
                is_not_found = False
                shop.open_hours.mon_st = dict_schedule['Пн'][0]
                shop.open_hours.mon_fn = dict_schedule['Пн'][1]
                shop.open_hours.tue_st = dict_schedule['Вт'][0]
                shop.open_hours.tue_fn = dict_schedule['Вт'][1]
                shop.open_hours.wed_st = dict_schedule['Ср'][0]
                shop.open_hours.wed_fn = dict_schedule['Ср'][1]
                shop.open_hours.thu_st = dict_schedule['Чт'][0]
                shop.open_hours.thu_fn = dict_schedule['Чт'][1]
                shop.open_hours.fri_st = dict_schedule['Пт'][0]
                shop.open_hours.fri_fn = dict_schedule['Пт'][1]
                shop.open_hours.sat_st = dict_schedule['Сб'][0]
                shop.open_hours.sat_fn = dict_schedule['Сб'][1]
                shop.open_hours.sun_st = dict_schedule['Вс'][0]
                shop.open_hours.sun_fn = dict_schedule['Вс'][1]
                shop.open_hours.save()
        if is_not_found:
            print(f'Не удалось найти магазин для этого адреса \"{address}\"')


    def save_price(self, address, dict_discounts):
        # print(address)
        # for key, value in dict_discounts.items():
        #     print(key, value)
        dict_week = {
            'Пн': [],
            'Вт': [],
            'Ср': [],
            'Чт': [],
            'Пт': [],
            'Сб': [],
            'Вс': [],
        }

        for key, value in dict_discounts.items():
            i = 0
            j = 0
            id_str = str()
            while True:
                if i == len(self.__list_discounts):
                    i = 0
                if value[j] == self.__list_discounts[i].promotion_name:
                    id_str += str(self.__list_discounts[i].id)
                    if j < len(value) - 1:
                        j += 1
                        if value[j] == '':
                            break
                    else:
                        break
                    id_str += '*'
                i += 1
            dict_week[key] = id_str
        # print('Работаем со скидками по адресу', address)
        # for key, value in dict_week.items():
        #     print(key, value)
        for sh in self.__list_stores:
            if sh.address == address:
                sh.promotion_days.monday = dict_week['Пн']
                sh.promotion_days.tuesday = dict_week['Вт']
                sh.promotion_days.wednesday = dict_week['Ср']
                sh.promotion_days.thursday = dict_week['Чт']
                sh.promotion_days.friday = dict_week['Пт']
                sh.promotion_days.saturday = dict_week['Сб']
                sh.promotion_days.sunday = dict_week['Вс']
                sh.promotion_days.save()