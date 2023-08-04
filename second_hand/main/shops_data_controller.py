from .data_processing import ModaMaxParserDataProcessor
from .data_save import ShopsDataDBSaver


class ShopsDataController:
    def __int__(self):
        self.list_shops = list()

    def start(self):
        self.list_shops = ModaMaxParserDataProcessor().get_parsing_results()  # вернули список магазинов в виде объектов
        self.data_save()

    def data_save(self):
        save_base = ShopsDataDBSaver()
        for shop in self.list_shops:
            save_base.save_datetime_work(shop.address, shop.dict_schedule)
            save_base.save_price(shop.address, shop.dict_discounts)