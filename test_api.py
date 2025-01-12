import pytest
import json
import requests
import allure
from const import *
from class_api import ApiKino

api_kino = ApiKino()


@allure.title('Поиск фильма по длинному слову')
@allure.description('Поиск фильма по длинному слову "' + long_name + '"')
@allure.severity(allure.severity_level.NORMAL)
def test_search_longname():
    with allure.step('Формирование запроса'):
        cell_test = api_kino.get_video('/search?', '&query=', long_name)
    with allure.step('Обнаружено одно совпадение'):
        assert cell_test.json()['total'] == 1
    with allure.step('Искомая строка входит в полученный ответ'):
        assert (long_name in cell_test.json()['docs'][0]['name']) is True


@allure.title('Поиск фильма по стране')
@allure.description('Поиск фильма по стране ' + country)
@allure.severity(allure.severity_level.NORMAL)
def test_search_country():
    with allure.step('Формирование запроса'):
        cell_test = api_kino.get_video('?', '&countries.name=', country)
    with allure.step('Найдено ' +
                     str(cell_test.json()['total']) + 
                     ' вхождений'):
        assert cell_test.json()['total'] > 1


@allure.title('Поиск фильма за невалидный период')
@allure.description('Поиск фильма за период ' + period)
@allure.severity(allure.severity_level.NORMAL)
def test_search_period():
    with allure.step('Формирование запроса'):
        cell_test = api_kino.get_video('?', '&year=', period)
    with allure.step('Статус запроса:' + 
                     str(cell_test.status_code) + ''):
        assert cell_test.json()['message'] == diap


@allure.title('Некорректно задан номер типа фильма')
@allure.description('Некорректно задан номер типа фильма')
@allure.severity(allure.severity_level.CRITICAL)
def test_search_tip():
    with allure.step('Формирование запроса'):
        cell_test = api_kino.get_video('?', '&typeNumber=', '0')
    with allure.step('Статус запроса:' + str(cell_test.status_code)):
        assert cell_test.json()['message'] == tip_f


@allure.title('Некорректное значение дробная часть рейтинга Кинопоиск')
@allure.description('Некорректно введена дробная часть рейтинга Кинопоиск')
@allure.severity(allure.severity_level.NORMAL)
def test_search_drob():
    with allure.step('Формирование запроса'):
        cell_test = api_kino.get_video('?', '&rating.kp=', '7,2')
    with allure.step('Статус запроса:' + str(cell_test.status_code)):
        assert cell_test.json()['message'] == drob