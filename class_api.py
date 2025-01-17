"""Этот модуль содержит классы и функции для взаимодействия с API киносайта."""

import allure
import requests
from const import api_key, url_k, page, limit

with allure.step("Сохранение ключа API"):
    headers = {"accept": "application/json", "X-API-KEY": api_key}


class ApiKino:
    """Классы для работы с API киносайта."""

    def __init__(self, url=url_k):
        """Инициализирует объект с заданным URL.

        Args:
            url: URL для запросов. По умолчанию используется url_k.
        """
        with allure.step("Установка пути запроса" + url):
            self.url = url

    def get_video(self, search, param, stroka):
        """Поиск видео по заданным параметрам."""
        with allure.step("Отправка запроса" + param):
            response = requests.get(
                self.url + search + "page="
                + page + "&limit=" + limit + param + stroka,
                headers=headers,
            )
        with allure.step("Сохранение результата запроса " + param):
            return response
