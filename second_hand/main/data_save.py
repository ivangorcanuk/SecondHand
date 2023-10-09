from .models import Stores, PromotionsRegister, OpenHours, PromotionDays


class ShopsDataDBSaver:
    list_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    def __init__(self):
        self.__list_stores = Stores.objects.all()
        self.__list_discounts = PromotionsRegister.objects.all()

    def save_datetime_work(self, network_name, address, dict_schedule):
        is_not_found = True
        for shop in self.__list_stores:
            if shop.address == address.strip() and shop.name_store == network_name:
                is_not_found = False
                shop.open_hours.mon_st = dict_schedule[self.list_week[0]][0]
                shop.open_hours.mon_fn = dict_schedule[self.list_week[0]][1]
                shop.open_hours.tue_st = dict_schedule[self.list_week[1]][0]
                shop.open_hours.tue_fn = dict_schedule[self.list_week[1]][1]
                shop.open_hours.wed_st = dict_schedule[self.list_week[2]][0]
                shop.open_hours.wed_fn = dict_schedule[self.list_week[2]][1]
                shop.open_hours.thu_st = dict_schedule[self.list_week[3]][0]
                shop.open_hours.thu_fn = dict_schedule[self.list_week[3]][1]
                shop.open_hours.fri_st = dict_schedule[self.list_week[4]][0]
                shop.open_hours.fri_fn = dict_schedule[self.list_week[4]][1]
                shop.open_hours.sat_st = dict_schedule[self.list_week[5]][0]
                shop.open_hours.sat_fn = dict_schedule[self.list_week[5]][1]
                shop.open_hours.sun_st = dict_schedule[self.list_week[6]][0]
                shop.open_hours.sun_fn = dict_schedule[self.list_week[6]][1]
                shop.open_hours.save()
        if is_not_found:
            print(f'Не удалось найти магазин для этого адреса \"{address}\"')

    def save_price(self, network_name, address, dict_discounts):
        dict_id_discounts = self.get_id_discounts(network_name, dict_discounts)
        for sh in self.__list_stores:
            if sh.address == address.strip() and sh.name_store == network_name:
                sh.promotion_days.monday = dict_id_discounts[self.list_week[0]]
                sh.promotion_days.tuesday = dict_id_discounts[self.list_week[1]]
                sh.promotion_days.wednesday = dict_id_discounts[self.list_week[2]]
                sh.promotion_days.thursday = dict_id_discounts[self.list_week[3]]
                sh.promotion_days.friday = dict_id_discounts[self.list_week[4]]
                sh.promotion_days.saturday = dict_id_discounts[self.list_week[5]]
                sh.promotion_days.sunday = dict_id_discounts[self.list_week[6]]
                sh.promotion_days.save()

    def get_id_discounts(self, network_name, dict_discounts):
        dict_id_discounts = dict()
        for key, value in dict_discounts.items():
            str_id = str()
            for discount in self.__list_discounts:
                for disc in value:
                    if discount.promotion_name == disc:
                        if discount.store_network == network_name or discount.store_network is None:
                            if str_id != '':
                                str_id += '*'
                            str_id += str(discount.id)
            dict_id_discounts[key] = str_id
        return dict_id_discounts
