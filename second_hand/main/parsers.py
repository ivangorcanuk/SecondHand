import requests
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime, date, timedelta


class ModaMaxParser:
    url = 'https://modamax.by/shops'
    headers = {
        'Accept': 'image/avif,image/webp,*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
    }

    def __init__(self):
        self.url_minsk_shop = self.get_url_all_shops_network()
        self.dikt_url_minsk_shops = self.get_url_all_shops(self.url_minsk_shop)
        self.dict_shop_data = self.get_data(self.dikt_url_minsk_shops)

    def get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        minsk_shop = soup.find(class_="shops__link")
        link_minsk_shop = 'https://modamax.by/' + minsk_shop.get('href')
        return link_minsk_shop

    def get_url_all_shops(self, url_minsk_shop):  # вернули словарь магазинов города Минска
        req_1 = requests.get(url_minsk_shop, headers=self.headers)
        soup_1 = BS(req_1.content, 'lxml')
        link_shops = soup_1.find_all(class_="shopCard")
        dict_shop = dict()  # словарь для хранения магазинов, ключ - адрес, значение - ссылка
        for i in link_shops:
            street_house = re.search(r'Минск, (.+)  \n', i.text)  # SOS
            #print(f'Тута \"{street_house.group(1)}\"')
            dict_shop[street_house.group(1)] = 'https://modamax.by/' + i.get('href')
        return dict_shop

    def get_data(self, dikt_url_minsk_shops):
        #symbols = [', ', ' ']
        count = 0
        dict_shop_data = dict()
        for key, value in dikt_url_minsk_shops.items():
            #if count < 2:
            # for i in symbols:
            #     if i in key:
            #         key = key.replace(i, '_')
            req_2 = requests.get(value, headers=self.headers)
            soup_2 = BS(req_2.content, 'lxml')
            open_hours = soup_2.find(class_='shopInfo__row-content')
            title = soup_2.find_all(class_='shopPrice__cell')
            title.append(open_hours)
            dict_shop_data[key] = title
            #print(key)
            count += 1
        return dict_shop_data


class EconomCity:
    pass


class Adzenne:
    pass


class Megahand:
    pass
