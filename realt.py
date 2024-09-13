import sqlite3
import requests
from config import token, chat_id


def format_text(offer):
    title = f'{offer['rooms']}-к квартира, {offer['area']}м², {offer['floor']}/{offer['totalfloor']} эт.'
    date = offer['date']
    #date = f'{d[0:2].d[4:6]} в {d[16:19]}'

    text = f"""
    {offer['price']} рублей\n
    <a href='{offer['url']}'>{title}</a>\n
    {offer['address']}\n
    {date}
    """
    return text

def send_telegram(offer):
    text = format_text(offer)
    url=f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url=url, data=data)
    print(response)

    #print(text)
def check_database(offer):
    offer_id=offer["offer_id"]

    with sqlite3.connect('.venv/db/realt.db')as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT offer_id FROM offers WHERE offer_id= (?)",
                       (offer_id, ))
        result=cursor.fetchone()
        print('222')
        if result is None:
            print('333')
            send_telegram(offer)
            print('rabotaem')

            cursor.execute("""
                        INSERT INTO offers
                        VALUES (NULL, :url, :offer_id, :date, :price, 
                        :address, :area, :rooms, :floor, :totalfloor)
                    """, offer)
            connection.commit()
            print(f'Объявление {offer_id} добавлено в базу данных')
        else:
            print('fuckkkkk')

# def main(offer):
#     check_database(offer)
#
# if __name__ == "__main__":
#     main(offer)