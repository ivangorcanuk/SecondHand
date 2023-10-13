from .data_processing import ModaMaxParserDataProcessor, EconomCityParserDataProcessor, AdzenneParserDataProcessor, MegahandParserDataProcessor
from .data_save import ShopsDataDBSaver


class ShopsDataController:
    def __init__(self):
        self.mmx_data_processor = ModaMaxParserDataProcessor()
        self.ec_data_processor = EconomCityParserDataProcessor()
        self.ad_data_processor = AdzenneParserDataProcessor()
        self.mh_data_processor = MegahandParserDataProcessor()
        self.dict_shops = dict()

    def start(self):
        self.dict_shops[self.mmx_data_processor.get_network_name()] = self.mmx_data_processor.get_parsing_results()
        # self.dict_shops[self.ec_data_processor.get_network_name()] = self.ec_data_processor.get_parsing_results()
        # self.dict_shops[self.ad_data_processor.get_network_name()] = self.ad_data_processor.get_parsing_results()
        # self.dict_shops[self.mh_data_processor.get_network_name()] = self.mh_data_processor.get_parsing_results()
        self.data_save()

    def data_save(self):
        save_base = ShopsDataDBSaver()
        for key in self.dict_shops.keys():
            for shop in self.dict_shops[key]:
                save_base.save_datetime_work(key, shop.address, shop.dict_schedule)
                save_base.save_price(key, shop.address, shop.dict_discounts)