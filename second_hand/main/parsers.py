import requests
from bs4 import BeautifulSoup as BS
import re
import json
from datetime import datetime, date, timedelta


class ModaMaxParser:
    url = 'https://modamax.by/shops'
    headers = {
        'Accept': 'image/avif,image/webp,*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
    }

    def __init__(self):
        self.__url_minsk_shop = None
        self.__dikt_url_minsk_shops = None

    def __get_url_all_shops_network(self):  # вернули ссылку со всеми магазинами города Минска
        req = requests.get(self.url, headers=self.headers)
        soup = BS(req.content, 'lxml')
        minsk_shop = soup.find(class_="shops__link")
        link_minsk_shop = 'https://modamax.by/' + minsk_shop.get('href')
        return link_minsk_shop

    def __get_url_all_shops(self, url_minsk_shop):  # вернули словарь магазинов города Минска
        req_1 = requests.get(url_minsk_shop, headers=self.headers)
        soup_1 = BS(req_1.content, 'lxml')
        link_shops = soup_1.find_all(class_="shopCard")
        dict_shop = dict()  # словарь для хранения магазинов, ключ - адрес, значение - ссылка
        for i in link_shops:
            street_house = re.search(r'Минск, (.+)  \n', i.text)
            #print(f'Тута \"{street_house.group(1)}\"')
            dict_shop[street_house.group(1)] = 'https://modamax.by/' + i.get('href')
        return dict_shop

    def get_data(self):
        self.__url_minsk_shop = self.__get_url_all_shops_network()
        self.__dikt_url_minsk_shops = self.__get_url_all_shops(self.__url_minsk_shop)
        count = 0
        dict_shop_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            req_2 = requests.get(value, headers=self.headers)
            soup_2 = BS(req_2.content, 'lxml')
            open_hours = soup_2.find(class_='shopInfo__row-content')
            list_prices = soup_2.find_all(class_='shopPrice__cell')
            list_prices.append(open_hours)
            dict_shop_data[key] = list_prices
            count += 1
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
        all_shop = soup.find(class_='shops__list not-list')
        all_shop1 = all_shop.find_all(class_='shops__link')
        dict_shop = dict()
        for i in all_shop1:
            if i.text == '\n':
                continue
            dict_shop[i.text.replace('\n', '')] = 'https://secondhand.by/' + i.get('href')
        return dict_shop

    def get_data(self):
        self.__dikt_url_minsk_shops = self.__get_url_all_shops_network()
        count = 0
        dict_shop_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            #if key == 'Рокоссовского, 49':  # Рокоссовского, 49
            req_1 = requests.get(value, headers=self.headers)
            soup_1 = BS(req_1.content, 'lxml')
            work_time = soup_1.find(class_="shopMap__info-description")
            all_calendar = soup_1.find("tbody")
            list_days = all_calendar.find_all("td")
            # f = all_work_time.text.replace('\n', '')  # получили склеиную строку
            list_days.append(work_time)
            dict_shop_data[key] = list_days
            count += 1
        return dict_shop_data


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
                a = i.find_all('a')
                all_shop_link.append(a[1])
            if 'Салігорск' in i.text:
                break
        dict_shop = dict()
        for i in all_shop_link:
            dict_shop[i.text] = i.get('href')
            #print(i.text, i.get('href'))
        return dict_shop

    def get_data(self):
        self.__dikt_url_minsk_shops = self.__get_url_all_shops_network()
        count = 0
        dict_shop_data = dict()
        for key, value in self.__dikt_url_minsk_shops.items():
            #if key == 'Крама па вул. В. Харужай, 8':
            #if count < 1:
            req_1 = requests.get(value, headers=self.headers)
            soup_1 = BS(req_1.content, 'lxml')
            working_month = soup_1.find('tbody', class_="simcal-month simcal-month-8")
            list_all_calendar = working_month.find_all("td")
            all_calendar = soup_1.find('div', class_="wpb_wrapper")
            work_time = re.search(r'Крама працуе:\n*(.+\n*.*)\n*Прыпынак', all_calendar.text)
            list_all_calendar.append(work_time.group(1))
            dict_shop_data[key] = list_all_calendar
            count += 1
        return dict_shop_data


