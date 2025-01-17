"""Этот модуль содержит классы и функции для UI проверок киносайта."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import allure


class KinoUi:
    """Класс для работы с UI киносайта."""

    def __init__(self, browser):
        """Инициализирует объект UI.

        Args:
            browser: Объект веб-драйвера.
        """
        self.browser = browser
        self.search_button = (By.CSS_SELECTOR, "input[value='поиск']")

    def vvod_text(self, by, identifier, text):
        """Метод для ввода текста в указанное поле."""
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((by, identifier))
        )
        element.clear()
        element.send_keys(text)

    def click_search_button(self):
        """Метод для нажатия на кнопку поиска."""
        self.browser.find_element(*self.search_button).click()

    def select_count_list(self, by, dropdown_id, option_xpath):
        """Метод выпадающего списка."""
        dropdown = self.browser.find_element(by, dropdown_id)
        dropdown.click()
        option = self.browser.find_element(By.XPATH, option_xpath)
        option.click()

    def wait_elem(self, by, value, timeout=8):
        """Метод ожидания элемента на странице."""
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            raise AssertionError(f"""Элемент {value} не найден
                                  за {timeout} секунд.""")

    def wait_text(self, by, value, text, timeout=15):
        """Метод ожидания появления текста в поле ввода на странице."""
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
        except TimeoutException:
            """Сообщение об ошибке при отсутствии текста
            в течение заданного времени"""
            print(
                f"Элемент с локатором {by} и значением {value},"
                "содержащий текст '{text}', "
                "не найден после {timeout} секунд."
            )
            return False

    def search_kind(self, kind):
        """Поиск по жанру."""
        kind_find = self.browser.find_element(
            By.XPATH, f"//input[@value='{kind}'] | //option[text()='{kind}']"
        )
        kind_find.click()
        self.click_search_button()

    def search_country(self, country):
        """Поиск по стране производства."""
        # Выбор страны из
        # выпадающего списка
        text_l = "//option[@value='"
        +country + "' or text()='" + country + "']"
        print(text_l)
        self.select_count_list(By.ID, "country", text_l)
        self.click_search_button()

    def search_year(self, year):
        """Поиск по году выпуска."""
        self.vvod_text(By.ID, "year", str(year))
        self.click_search_button()

    def random_poisk(self):
        """Запуск случайного поиска по ранее заполненным параметрам."""
        with allure.step(
                         "Нажитие кнопки поиска на главной странице."):
            self.browser.find_element(By.CSS_SELECTOR,
                                      "button[type='submit']").click()
        with allure.step(
                         'Нажитие кнопки "Случайный поиск"'):
            self.browser.find_element(By.ID, "search").click()
        with allure.step("Сайт отобразил случайный фильм"):
            res = self.browser.find_element(By.CLASS_NAME, "filmName")
        # Получено названия фильма
        return res.find_element(By.CSS_SELECTOR, "a").get_attribute("text")

    # Авторизация на сайте
    @allure.step("Переход на сайт Кинопоиск, с последующей авторизацией.")
    def user_auth(self, login: str, password: str):
        """Авторизация пользователя."""
        with allure.step(
                         "Проверка на CAPTCHA"):
            try:
                with allure.step(
                        "Подтверждение CAPTCHA, переход к авторизации"):
                    self.browser.find_element(
                        By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
                    ).click()
            except NoSuchElementException:
                with allure.step("Переход к следующему этапу"):
                    pass

        with allure.step(
                         "Нажитие кнопки 'Войти' на главной странице сайта."):
            self.browser.find_element(
                By.CSS_SELECTOR, ".styles_loginButton__LWZQp"
            ).click()

        with allure.step("Ввод адреса электронной почты (логин)."):
            self.browser.find_element(By.CSS_SELECTOR,
                                      "#passp-field-login").send_keys(
                login
            )

        with allure.step(
            "Нажитие кнопки 'Войти', на странице ввода логина пользователя."
        ):
            self.browser.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()

        with allure.step("Ввод пароля."):
            self.browser.find_element(By.CSS_SELECTOR,
                                      "#passp-field-passwd").send_keys(
                password
            )

        with allure.step(
            "Нажитие кнопки 'Войти', на странице ввода пароля пользователя."
        ):
            self.browser.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()
        with allure.step('Проверка доступности кнопки "Меню профиля"'):
            res = self.browser.find_element(By.CLASS_NAME,
                                            "styles_root__42Fk8")
            WebDriverWait(self.browser,
                          5).until(EC.element_to_be_clickable(res))
        return res.get_attribute("aria-label")
