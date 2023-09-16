import requests
from bs4 import BeautifulSoup as BS
import re
import json


class ModaMaxParser:
    url = 'https://modamax.by/shops'
    headers = {
        'Accept': 'image/avif,image/webp,*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
    }

    def __init__(self):
        self.__url_shops_in_minsk = None
        self.__dikt_url_minsk_shops = None

    def __get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        minsk_shop = soup.find(class_="shops__link")
        link_minsk_shop = 'https://modamax.by/' + minsk_shop.get('href')
        return link_minsk_shop

    def __get_url_all_shops(self, url_minsk_shop):  # вернули словарь магазинов города Минска
        req = requests.get(url_minsk_shop, headers=self.headers)
        soup = BS(req.content, 'lxml')
        link_shops = soup.find_all(class_="shopCard")
        dict_shops = dict()  # словарь для хранения магазинов, ключ - адрес, значение - ссылка
        for i in link_shops:
            street_house = re.search(r'Минск, (.+)  \n', i.text)
            dict_shops[street_house.group(1)] = 'https://modamax.by/' + i.get('href')
        return dict_shops

    def get_data(self):
        self.__url_shops_in_minsk = self.__get_url_all_shops_network()
        self.__dikt_url_minsk_shops = self.__get_url_all_shops(self.__url_shops_in_minsk)
        dict_shop_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            req = requests.get(value, headers=self.headers)
            soup = BS(req.content, 'lxml')
            open_hours = soup.find(class_='shopInfo__row-content')
            list_prices = soup.find_all(class_='shopPrice__cell')
            list_prices.append(open_hours)
            dict_shop_data[key] = list_prices
        return dict_shop_data


class EconomCityParser:
    url = 'https://secondhand.by/shops.html'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
    }

    def __init__(self):
        self.__dikt_url_minsk_shops = None

    def __get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        shops_block = soup.find(class_='shops__list not-list')
        all_shops = shops_block.find_all(class_='shops__link')
        dict_shops = dict()
        for i in all_shops:
            if i.text != '\n':
                dict_shops[i.text.replace('\n', '')] = 'https://secondhand.by/' + i.get('href')
        return dict_shops

    def get_data(self):
        self.__dikt_url_minsk_shops = self.__get_url_all_shops_network()
        dict_shops_data = dict()
        i = 0
        for key, value in self.__dikt_url_minsk_shops.items():
            #if i < 1:
            i += 1
            req = requests.get(value, headers=self.headers)
            soup = BS(req.content, 'lxml')
            open_hours = soup.find(class_="shopMap__info-description")
            calendar_block = soup.find("tbody")
            list_days = calendar_block.find_all("td")
            list_days.append(open_hours)
            dict_shops_data[key] = list_days
        return dict_shops_data


class AdzenneParser:
    url = 'https://second-hand.by/kramy/'
    headers = {
        'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
    }

    def __init__(self):
        self.__dikt_url_minsk_shops = None

    def __get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        all_shop = soup.find_all(class_='wpb_text_column wpb_content_element')
        all_shop_link = list()
        for i in all_shop:
            if 'Крама' in i.text:
                tags = i.find_all('a')
                all_shop_link.append(tags[1])
            if 'Салігорск' in i.text:
                break
        dict_shop = dict()
        for i in all_shop_link:
            dict_shop[i.text] = i.get('href')
        return dict_shop

    def get_data(self):
        self.__dikt_url_minsk_shops = self.__get_url_all_shops_network()
        dict_shop_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            req = requests.get(value, headers=self.headers)
            soup = BS(req.content, 'lxml')
            calendar_block = soup.find('table', class_="simcal-calendar-grid")
            list_all_days = calendar_block.find_all("td")
            all_calendar = soup.find('div', class_="wpb_wrapper")
            work_time = re.search(r'Крама працуе:\n*(.+\n*.*)\n*Прыпынак', all_calendar.text)
            list_all_days.append(work_time.group(1))
            dict_shop_data[key] = list_all_days
        return dict_shop_data


class MegahandParser:
    url = 'https://mega-hand.by/magaziny/minsk/'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
    }

    def __init__(self):
        self.__dikt_url_minsk_shops = None

    def __get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        all_shops = soup.find_all(class_='sity_magazin')
        dict_shops = dict()
        for url in all_shops:
            if 'магазин МЕГАХЕНД в Минске' in url.text:
                link = url.find('a', class_='public-life__image-link')
                address = url.find(class_='top_shop_blok_desc')
                dict_shops[address.text] = link.get('href')
        return dict_shops

    def get_data(self):
        self.__dikt_url_minsk_shops = self.__get_url_all_shops_network()
        dict_shops_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            req = requests.get(value, headers=self.headers)
            soup = BS(req.content, 'lxml')

            scripts_all = soup.find_all('script', type='text/javascript')
            list_of_dictionaries = None
            for script in scripts_all:
                script_str = str(script)
                if 'var data' in script_str:
                    script_calendar = script_str[script_str.catalog('['):script_str.catalog(']')+1]
                    list_of_dictionaries = json.loads(script_calendar)

            info_blocks = soup.find_all(class_="top_shop_blok")
            open_hours = None
            for block in info_blocks:
                if 'Ежедневно' in block.text:
                    open_hours = block.find(class_="top_shop_blok_desc")

            list_of_dictionaries.append(open_hours)
            dict_shops_data[key] = list_of_dictionaries

        return dict_shops_data
