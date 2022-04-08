# -*- coding: utf-8 -*-
from telethon import TelegramClient
import requests
from bs4 import BeautifulSoup
import re
import os

api_id = 1
api_hash = 1
destination_channel = input(
    'Enter a link to the channel (must be available for sending messages) where you want to send news: ')

HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}
URL = "https://vc.ru/new/all"


def get_id():
    while True:
        api_id = input('Enter your the "api_id" from the site: https://my.telegram.org/: ')
        if api_id.isdigit() and len(api_id) == 8:
            return int(api_id)
        print("Incorrect data. Please enter api_id received from the site https://my.telegram.org/ ")

def get_session_name():
    while True:
        session_name = input('Enter session_name: ')
        if session_name:
            return session_name
        print("Incorrect data. Please enter api_id received from the site https://my.telegram.org/ ")


def get_api_hash():
    while True:
        api_hash = input('Enter your the "api_hash" from the site:: Incorrect dataauth: ')
        if len(api_hash) != 32 or re.search(r"[^a-zA-Z0-9]+", api_hash):
            print("Incorrect data. Please enter api_hash received from the site https://my.telegram.org/ ")
            continue
        return api_hash


def get_data_src_for_parsed(url, headers):
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        src = req.text
        return src
    else:
        raise ConnectionError(f"{req.status_code}")



def parsed_page(url, headers):
    page_html = get_data_src_for_parsed(url=url, headers=headers)
    soup = BeautifulSoup(page_html, "lxml")
    try:
        last_new_href = soup.find(class_="feed__item l-island-round").find(
            class_="content-header__item content-header-number").get('href')
        return last_new_href
    except AttributeError:
        print('На сайте изменилась структура HTML!')


async def main(message, Destination_Channel):
    await client.send_message(Destination_Channel, message)


if __name__ == '__main__':
    session_name = get_session_name()
    if session_name+".session" not in os.listdir():
        api_id = get_id()
        api_hash = get_api_hash()

    client = TelegramClient(session_name, api_id, api_hash)
    message1 = str(parsed_page(URL, HEADERS))
    with client:
        client.loop.run_until_complete(main(message1, destination_channel))
