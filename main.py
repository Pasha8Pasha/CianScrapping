import requests
import json
import datetime
from datetime import datetime
import time
import sqlite3
from realt import check_database

def get_offer(item):
    offer = {}

    offer["url"]= item["fullUrl"]
    offer["offer_id"] = item["id"]

    timestamp = datetime.fromtimestamp(item["addedTimestamp"])
    timestamp = datetime.strftime(timestamp, '%d.%m.%Y  в  %H:%M')
    offer["date"]=timestamp

    offer["price"]=item["bargainTerms"]["priceRur"]
    offer["address"]=item["geo"]["userInput"]
    offer["rooms"]=item["roomsCount"]
    offer["area"]=item["totalArea"]
    offer["floor"]=item["floorNumber"]
    offer["totalfloor"]=item["building"]["floorsCount"]
    offer["opis"] = item["title"]

    print(offer)
    return offer

def get_offers(data):
    #offers=[]

    for item in data ["data"] ["offersSerialized"]:
        offer = get_offer(item)
        check_database(offer)
        print('111')


def get_json():

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        # 'cookie': '_CIAN_GK=0a12a1f0-639d-46fb-976d-064db563f1d0; _gcl_au=1.1.1373985257.1718632171; tmr_lvid=5421c7c568acc47e7e56348464d74d12; tmr_lvidTS=1718632172581; login_mro_popup=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; uxfb_usertype=searcher; _ym_uid=1718632177148500898; _ym_d=1718632177; _gid=GA1.2.1275492323.1718632177; uxs_uid=6f9a8ac0-2cb0-11ef-a9fb-1b8c2cd42b5d; _ym_isad=2; adrdel=1718632177740; adrcid=Au4i3FSzOTUDuPup3ar4lxA; afUserId=88869bcd-241e-4add-8e59-ddc7f9753398-p; AF_SYNC=1718632177873; session_region_id=1; session_main_town_region_id=1; _ga=GA1.2.1961588116.1718632177; _ga_3369S417EL=GS1.1.1718632176.1.1.1718633880.60.0.0; __cf_bm=wf1btHATEBU7Y7XV2trq9BhZTBRZABVgdXwFYWD4MxA-1718635895-1.0.1.1-JpdE9JDCwSHauvHiF4Bf9Z3V0724H5Jcse_UO47oWaWeraZkSfMUc1CDAWvYsNlrI65hURYv_wxW8fRgdeplzg',
        'origin': 'https://www.cian.ru',
        'priority': 'u=1, i',
        'referer': 'https://www.cian.ru/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    json_data = {
        'jsonQuery': {
            '_type': 'flatrent',
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'region': {
                'type': 'terms',
                'value': [
                    1,
                ],
            },
            'price': {
                'type': 'range',
                'value': {
                    'lte': 80000,
                },
            },
            'currency': {
                'type': 'term',
                'value': 2,
            },
            'for_day': {
                'type': 'term',
                'value': '!1',
            },
            'room': {
                'type': 'terms',
                'value': [
                    1,
                    2,
                    9,
                ],
            },
            'total_area': {
                'type': 'range',
                'value': {
                    'gte': 35,
                },
            },
        },
    }

    response = requests.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        headers=headers,
        json=json_data,
    )
    try:
        result = response.json()
        return result
    except json.JSONDecodeError as e:
        print(f"Ошибка: {e}")
    else:
        print("JSON строка пуста")

   # print(data)
   # with open('data.json', 'w', encoding='utf-8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    data=get_json()

    get_offers(data)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(50)

