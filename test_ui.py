from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import allure
from const import *


@allure.feature("Авторизация на сайте")
@allure.title("Тест авторизации пользователя.")
@allure.description("Авторизуемся на сайте используя входные данные.")
@allure.severity(allure.severity_level.BLOCKER)
def test_ui_vhod(search_kino_ui):
    logon = search_kino_ui.user_auth(login, password)
    assert logon == 'Меню профиля'


@allure.feature("Поиск случайного фильма")
@allure.title("Поиск случайного фильма")
@allure.description("Проверка случайного поиска фильмов без условий")
@allure.severity(allure.severity_level.NORMAL)
def test_ui_poisk(search_random_ui):
    rand = search_random_ui.random_poisk()
    with allure.step('Случайный фильм отображается'):
        assert rand is not None


@allure.feature("Поиск фильмов по году")
@allure.title("Поиск случайного фильма без фильтра")
@allure.description("Проверка поиска фильмов, произведенных в " +
                    year_s + "г.")
@allure.severity(allure.severity_level.NORMAL)    
def test_search_year(search_main):
    with allure.step(f'Поиск по году выпуска: {year_s}'):
        search_main.search_year(year_s)

    with allure.step("Проверка происхождения найденного контента "
                     "в " + year_s + " год"):
        year_find = search_main.wait_text(
            By.CLASS_NAME, 'year', year_s)

    assert year_find, ("Expected to find content " + year_s)


@allure.feature("Поиск фильмов по жанру")
@allure.title("Поиск фильмов по фильтру Жанр")
@allure.description("Проверка поиска фильмов,у которых в списке жанров есть" +
                    kind_s)
@allure.severity(allure.severity_level.NORMAL) 
def test_search_kind(search_main):
    with allure.step("Поиск контента по жанру 'детектив'"):
        search_main.search_kind(kind_s)

    kind_p = f"//span[@class='gray' and contains(., '{kind_s}')]"

    with allure.step("Проверка, что найденное относится к жанру " +
                     kind_s):
        kind_found = search_main.wait_text(By.XPATH, kind_p, kind_s)

    assert kind_found is True


@allure.feature("Поиск фильмов по стране")
@allure.title("Поиск фильмов по фильтру Страна")
@allure.description(f"Проверка поиска фильмов со страной {country_s}")
@allure.severity(allure.severity_level.NORMAL) 
def test_search_country(search_main):
    with allure.step(f"Поиск по стране {country_s}"):
        search_main.search_country(country_s)

    with allure.step(f"Проверка присутсвия соответствует стране {country_s}"):
        country = search_main.wait_elem(By.CLASS_NAME, "text-blue").text

    assert country == ("«" + country_s + "»")