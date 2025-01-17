"""Этот модуль содержит фикстуры для тестов.

Фикстуры предоставляют тестовые данные и ресурсы.
"""

import pytest
from selenium import webdriver
from class_ui import KinoUi
from const import url_b


@pytest.fixture()
def driver():
    """Параметры драйвера."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def search_kino_ui(driver):
    """Переход на страницу Кинопоиска."""
    driver.get(url_b)
    return KinoUi(driver)


@pytest.fixture
def search_random_ui(driver):
    """Осуществление поиска по сайту."""
    driver.get(url_b + "/chance/")
    return KinoUi(driver)


@pytest.fixture
def search_main(driver):
    """Переход на страницу поиска и создание обьекта."""
    driver.get(url_b + "/s/")
    return KinoUi(driver)
