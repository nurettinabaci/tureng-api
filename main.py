import json
import requests
from bs4 import BeautifulSoup
import re
REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 "
                  "Safari/537.36"}
language = {"EN-TR":"turkce-ingilizce",
            "EN-DE":"almanca-ingilizce",
            "EN-ES":"ispanyolca-ingilizce",
            "EN-FR":"fransizca-ingilizce",
            "İngilizce Eşanlam":"ingilizce-esanlam"}

TURENG_URL = r'https://tureng.com/tr/'

family_list = {'f. ':'fiil',
               's. ':'sıfat',
               'i. ':'isim',
               ' '  : 'bileşik',
               }

def create_url(word):
    global TURENG_URL
    word = "%20".join(re.findall(r'[a-z0-9]+', word))
    base_url = "".join((TURENG_URL, language.get("EN-TR"), '/', word))
    return base_url

def html_request(link):
    return requests.get(link, headers=REQUEST_HEADER)

def store_to_json():
    pass

def word_family(word):
    family_of_the_word = family_list.get(word[0])
    return family_of_the_word

def get_result(a_word):
    target_url = create_url(a_word)
    page_response = html_request(target_url)
    soup_detail = BeautifulSoup(page_response.text, "html.parser")
    return soup_detail

soup_result = get_result('a half-wit')
table_result = soup_result.find_all('table', id="englishResultsTable")
english_content = table_result[0].find_all('td', class_ = 'en tm')
order = table_result[0].find_all('td', class_='rc0 hidden-xs')
meaning = table_result[0].find_all('td', class_ = 'tr ts')


for x, y, z in zip(order, english_content, meaning):
    print(x.text , word_family(y.i.contents), z.contents[0].text)


