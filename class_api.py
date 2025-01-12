import json
import allure
import requests
from const import *

with allure.step('Сохранение ключа API'):
    headers = {"accept": "application/json",
               "X-API-KEY": api_key}


class ApiKino:
    def __init__(self, url=url_k):
        with allure.step('Установка пути запроса' + url):
            self.url = url
    
    def get_video(self, search, param, stroka):
        with allure.step('Отправка запроса' + param):
            response = requests.get(self.url + search + 'page=' + 
                                    page + '&limit=' + limit + param +
                                    stroka, headers=headers)
        with allure.step('Сохранение результата запроса ' + param):
            return response