"""
    An API for www.tureng.com
    Author: Nurettin ABACI
    Modified: 2020-08-19
"""
import json
import requests
from bs4 import BeautifulSoup
import re
from typing import Literal
from fake_useragent import UserAgent


language = {"EN-TR": "turkce-ingilizce",
            "EN-DE": "almanca-ingilizce",
            "EN-ES": "ispanyolca-ingilizce",
            "EN-FR": "fransizca-ingilizce",
            "İngilizce Eşanlam": "ingilizce-esanlam"}

TURENG_URL = r'https://tureng.com/tr/'


family_list = {'f. ': 'fiil',
               's. ': 'sıfat',
               'i. ': 'isim',
               ' ': 'bileşik',
               }


class TurengAPI:
    """An API for accessing the meanings of a word in the order of importance
    from the www.tureng.com site.
    """
    def __init__(self, lang: Literal["en-tr", "en-de", "en-es", "en-fr"] = 'en-tr'):
        self.lang = lang

    @property
    def lang(self):
        return self.__lang

    @lang.setter
    def lang(self, lang: Literal["en-tr", "en-de", "en-es", "en-fr"]):
        self.__lang = lang

    def translate(self, word: str) -> None:
        page_soup = TurengAPI.__get_page_soup(word)
        table_result = page_soup.find_all('table', id="englishResultsTable")
        english_content = table_result[0].find_all('td', class_='en tm')
        order = table_result[0].find_all('td', class_='rc0 hidden-xs')
        meaning = table_result[0].find_all('td', class_='tr ts')

        for x, y, z in zip(order, english_content, meaning):
            print(x.text, TurengAPI.__word_family(y.i.contents), z.contents[0].text)
        # result_json = TurengAPI.__store_to_json()
        # return result_json

    @staticmethod
    def __store_to_json():
        """Stores the table result to a json variable.
        """
        pass

    @staticmethod
    def __word_family(word):
        """Extracts the family(noun,verb,adverb,????) of the word.
        """
        family_of_the_word = family_list.get(word[0])
        return family_of_the_word

    @staticmethod
    def __html_request(link):
        """Returns the html response with a fake
        """
        return requests.get(link, headers={'user-agent': UserAgent().random})

    @staticmethod
    def __create_url(word):
        global TURENG_URL
        word = "%20".join(re.findall(r'[a-z0-9]+', word))
        base_url = "".join((TURENG_URL, language.get("EN-TR"), '/', word))
        return base_url

    @staticmethod
    def __get_page_soup(a_word):
        target_url = TurengAPI.__create_url(a_word)
        page_response = TurengAPI.__html_request(target_url)
        if page_response.status_code != 200:
            raise requests.ConnectionError
        soup_detail = BeautifulSoup(page_response.text, "html.parser")
        return soup_detail
