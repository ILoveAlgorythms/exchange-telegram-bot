from datetime import datetime
import requests
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def cryptoexchange_parse_rate(from_name: str, to_name: str, r: int = 3, is_update: bool = False) -> float:
    """ Получает файл с курсами с сайта cryptoexchange.cc
        и извлекает ставки из выбранной валютной пары.

        Если пара не найдена, возвращает словарь
        с указанными параметрами и нулевым курсом.

        :from_name:     str отдаваемый актив
        :to_name:       str получаемый актив
        :r:             int округление

        :is_update: bool вызывается с таскером (обновляте файл с курсами)
    """
    from loader import cache, config, ROOT_DIR

    file_name = 'cryptoexchange-rates-export.xml'
    file_path = ROOT_DIR + '/data/files/'+ file_name
    rates_xml_file_link = 'https://cryptoxchange.cc/rates-export.xml?utm_source=bestchange'
    file_exist = Path(file_path).is_file()

    pair_rate = {
        'from': from_name,
        'to': to_name,
        'in': 0,
        'out': 0,
    }

    if is_update or file_exist is False:
        try:
            headers = {
                "Referer": "https://cryptoxchange.cc/partners",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            }
            cookies = {
                "cryptoxchange_session": "eyJpdiI6IndEYUduVS91cWdKVXRmM2QwVkJrSFE9PSIsInZhbHVlIjoiRE9GbEFTZS9kMmROSUNMMmx0V2htaU9FalZuV3hOSk9keEc4R0RTdjk1aTlhd2xCOWVPNFFyeW9majUvRXVnQjFUSU10VXZ6L0pDS0pGSFRIbFlDYU92em5HRFZJQTVyQ1lEV1Q5ZndSK1AwTlVnNCsyaUlpWmlDUmlyejArN04iLCJtYWMiOiJjZGFkZjU1MjRlMTZhZTBiMzk0MmEwZDk5YzYwYWRlNDhlMDQ5OGRlZmJjOTA1MDBkZTY2NzNmMWIyM2FkMTIxIiwidGFnIjoiIn0=",
                "XSRF-TOKEN": "eyJpdiI6IkJDRTdQZ3diWUxDNFhPY1NvUEZCV0E9PSIsInZhbHVlIjoianY3L1d1WDBYQ1NVYStFYmFHYkVEYk8xVTIyUHpiUmtZc1Y0a2tSRUhzV0l2QTRMZFRBb0UxcGd0NlVsYXV4TEE5NlFPdXZVbzlaMkg0bkU3dzBZYkZDZVF5KzVtbjNUUjRveGhMZWdGS3I4dFowRHJxZ1BCMU1FMHM3QmF6NVUiLCJtYWMiOiIxNWNhZTIyNDk5MDgxNzRjZmViNjk0ZDQzMmY2M2Q1NjNiNDdhMmRhMjViZWNjYTE1ZDlkZDM2OThjNWQwZTZmIiwidGFnIjoiIn0=",
                "__lhash_": "4469c2dce5189986e8dde7306008645b",
                "__hash_": "e4b9647a43b2cc121759d02792890256",
                "__jhash_": "431",
                "__js_p_": "194,1800,0,0,0",
            }
            rates = requests.get(rates_xml_file_link, headers=headers)
            xml = rates.text

            # > 500 - это просто условности
            # бывает что парсер отдаёт пустой файл
            # и это просто проверка на наличие инфы
            if len(rates.content) > 500 and rates.headers['content-type'] == 'application/xml':
                with open(file_path, encoding='utf-8', mode='w') as f:
                    f.write(xml)
                    print(f"[{datetime.now()}] Файл с курсами валют сайта cryptoexchange.cc обновлён")
        except Exception as e:
            print(e)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for pair in root.findall('item'):
            rate_from_name = pair.find('from').text
            rate_to_name = pair.find('to').text
            rate_in = pair.find('in').text
            rate_out = pair.find('out').text

            if (
                from_name == rate_from_name and
                to_name == rate_to_name
            ):
                pair_rate['in'] = round(float(rate_in), r)
                pair_rate['out'] = round(float(rate_out), r)

    except Exception as e:
        print(e)

    return pair_rate


def binance_p2p_arithmetic_mean_data(transAmount=500, fiat_asset='RUB', tradeType='SELL', payType='TinkoffNew', asset='USDT', rows=15, r=3):
    """ Возвращает среднее арифметическое курса обмена
        из списка ордеров на Binance P2P

        :transAmount: int Сумма
        :fiat_asset:  str Получаемая валюта
        :tradeType:   str Тип объявления SELL/BUY
        :payType:     str Slug платежной системы для фильтра
        :asset:       str Актив для обмена
        :rows:        int Количество объявлений для рассчёта
        :r:           int Округление числа
    """

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    data = {
      "asset": asset,
      "fiat": fiat_asset,
      "merchantCheck": False,
      "page": 1,
      "payTypes": [payType],
      "publisherType": None,
      "rows": rows,
      "tradeType": tradeType
    }
    ads = []

    try:
        data = requests.post(
            'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
            headers=headers,
            json=data
        )
        ads = data.json()
    except Exception as e:
        print(e)

    ads_count = len(ads['data'])
    sum = 0

    if ads_count > 0:
        price = 0
        for ad in ads['data']:
            price += float(ad['adv']['price'])
        # ОбщаяЦена / КоличествоОбъявлений
        sum = price / ads_count

    return round(sum, r)

def binance_get_price_pair(main_asset, proxy_asset, r=3):
    """ Возвращает валютный курс

        :main_asset:  str Актив-1
        :proxy_asset: str Актив-2
    """
    symbol = main_asset + proxy_asset
    special = ['RUBUSDT']

    if symbol in special:
        symbol = proxy_asset + main_asset

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "api.binance.com",
        "Origin": "https://api.binance.com/",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    symbol_info = {}

    try:
        data = requests.get(
            'https://api.binance.com/api/v3/ticker/price?symbol='+symbol,
            headers=headers
        )
        symbol_info = data.json()
    except Exception as e:
        print(e)

    price = symbol_info.get('price', 0)

    return round(float(price), r)

def binance_get_price_pair(main_asset, proxy_asset, r=2):
    """ Возвращает валютный курс

        :main_asset:  str Актив-1
        :proxy_asset: str Актив-2
    """
    symbol = main_asset + proxy_asset
    special = ['RUBUSDT']

    if symbol in special:
        symbol = proxy_asset + main_asset

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "api.binance.com",
        "Origin": "https://api.binance.com/",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    symbol_info = {}

    try:
        data = requests.get(
            'https://api.binance.com/api/v3/ticker/price?symbol='+symbol,
            headers=headers
        )
        symbol_info = data.json()
    except Exception as e:
        print(e)

    price = symbol_info.get('price', 0)

    return round(float(price), r)
