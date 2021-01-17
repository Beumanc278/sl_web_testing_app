import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Tester():
    """
    Создаем класс, который будет иметь необходимые функции для проведения автоматизированного теста и сохранять
    результаты каждого шага тестирования в таблице в excel-файле
    """
    def __init__(self):
        """
        При инициализации класса:
        1) Добавляются опции, например скрытие окна браузера во время проверки
        2) Запускается webdriver с выбранными опциями
        3) Формируется файл с логами работы программы, который записывается в папку /logs в корневой папке проекта,
        в имени файла фиксируется дата и время инициализации класса
        """
        # добавляем необходимые опции для webdriver
        self.options = Options()
        #self.options.add_argument('--headless') # скрываем окно браузера при запуске сервера, убрать # при необходимости
        # запускаем webdriver
        self.browser = webdriver.Chrome(r'.\chromedriver\chromedriver.exe', options=self.options)
        # переадресуем запись логов в файл в папке ./logs, в названии указываем время инициализации класса
        # настраиваем базовые настройки логгирования (вывод в консоль и в файл)
        file_log = logging.FileHandler(f'.\logs\log - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log')
        console_log = logging.StreamHandler()
        logging.basicConfig(handlers=(file_log, console_log),
                            level=logging.INFO,
                            format="%(asctime)s - %(message)s")
        self.logger = logging.getLogger()
        self.logger.info('Запущен webdriver')

        # создаем переменную для хранения ссылки на тестируемый сайт
        self.url = None

    def close_webdriver(self):
        """
        Функция завершает работу Web-драйвера. Применять после окончания работы.
        """
        self.browser.close()
        self.browser.quit()
        self.logger.info('Webdriver успешно завершил работу')

    def xpath_exists(self, url):
        """
        Функция проверяет, есть ли элемент на странице по xpath
        :param url: xpath до элемента
        :return: True/False, в зависимости от того, есть ли элемент
        """
        browser = self.browser
        try:
            element = browser.find_elements_by_xpath(url)[0]
            exist = True
            return exist, element
        except NoSuchElementException:
            exist = False
            return exist, None
        except Exception as ex:
            exist = False
            return exist, None

    def set_test_url(self, test_url):
        """
        Функция сохраняет в класс ссылку на тестируемый сайт, для использования в других функциях
        :param test_url: ссылка на тестируемый сайт
        """
        self.url = test_url
        self.logger.info(f'В Tester передана ссылка для тестирования - {test_url}')

    def authorization_test(self, id, login, password):
        """
        Функция производит тестирование процесса авторизации по переданным данным.
        Заполняет поля Email и Password переданными значениями, проверяет ошибки полей ввода,
        фиксирует их и возвращает для дальнейшей обработки
        :param id: id проверки
        :param login: логин для ввода
        :param password: пароль для ввода
        :return: status_dict - словарь, где ключ - Проверяемый параметр, значение - Состояние параметра и детали ошибки)
        """
        self.logger.info(f"Запущена функция authorization_test с параметрами Email = {login} и Password = {password}")
        status_dict = {}
        if self.url == None:
            self.logger.info('Ссылка не передана, отмена операции')
            return
        # заменяем входные значения nan из Excel на пустую строку
        if type(login) == float:
            login = ''
        if type(password) == float:
            password = ''
        self.browser.get(self.url) # переходим на тестируемый сайт
        # добавляем ожидание загрузки страницы сайта
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'signin-login')))
            status_dict['Страница успешно загружена'] = {'status': True, 'details': None}
        except:
            self.logger.info('Страница не была загружена в ходе сессии')
        # переводим форму в формат Sign in
        self.browser.execute_script("document.getElementsByClassName('fz-18')[3].click()")
        time.sleep(1)
        # получаем ссылки на поля формы для заполнения
        email_input = self.browser.find_element_by_id('signin-login')
        email_input.clear()
        password_input = self.browser.find_element_by_id('signin-pass')
        password_input.clear()
        # заполняем поля
        email_input.send_keys(login)
        password_input.send_keys(password)
        # проверяем поле ввода Email на наличие ошибок, фиксируем при наличии
        if 'error' in email_input.get_attribute('class'):
            error_div = self.browser.find_element_by_xpath("//div[@class='error']")
            error_text = error_div.text
            status_dict['Проверка поля Email'] = {'status': False, 'details': error_text}
        else:
            status_dict['Проверка поля Email'] = {'status': True, 'details': None}
        # проверяем поле ввода Password на наличие ошибок, фиксируем при наличии
        if 'error' in password_input.get_attribute('class'):
            error_div = self.browser.find_element_by_xpath("//div[@class='error-text']")
            error_text = error_div.text
            status_dict['Проверка поля Password'] = {'status': False, 'details': error_text}
        else:
            status_dict['Проверка поля Password'] = {'status': True, 'details': None}
        # находим элемент кнопки и проверяем ее статус
        submit_button = self.browser.find_element_by_xpath('//button[contains(text(), "Sign in")]')
        button_status = submit_button.get_attribute('disabled')
        if button_status == None:
            status_dict['Состояние кнопки'] = {'status': True, 'details': "Кнопка активна"}
        elif button_status == 'true':
            status_dict['Состояние кнопки'] = {'status': False, 'details': "Кнопка не активна"}
        # если поле Email и поле Password заполнены корректно, пробуем нажать на Sign in и проверяем корректность пары логин-пароль
        status_dict['Успешная авторизация'] = {'status': False, 'details': ''}
        if status_dict['Проверка поля Email']['status'] == True and status_dict['Проверка поля Password']['status'] == True and status_dict['Состояние кнопки']['status'] == True:
            submit_button.click()
            time.sleep(0.5)
            try:
                submit_error = self.browser.find_element_by_xpath('//*[@id="panel"]/main/div/div[1]/form/div[3]/div')
                status_dict['Успешная авторизация'] = {'status': False, 'details': submit_error.text}
            except:
                status_dict['Успешная авторизация'] = {'status': True, 'details': None}
                self.logger.info('Выполнена успешная авторизация и переход на главную страницу сайта')

        self.logger.info(f'В ходе проверки {int(id)} зафиксировано следующее состояние элементов тестирования:')
        for item in status_dict.items():
            self.logger.info(f'{item}')

        # если в ходе проверки произошла успешная авторизация, перезапускаем webdriver для сброса авторизации
        if status_dict['Успешная авторизация']['status'] == True:
            self.close_webdriver()
            # запускаем webdriver
            self.browser = webdriver.Chrome('./chromedriver/chromedriver.exe', options=self.options)
        return status_dict

    def authorize(self, login, password):
        """
        Функция выполняет авторизацию по корректным данным и переходит на главную страницу сайта
        :param login: корректный логин
        :param password: корректный пароль
        :return: True/False в зависимости от того, удалось ли перейти на главную страницу сайта
        """
        self.logger.info(f'Запущена функция авторизации пользователя с корректными данными')
        self.browser.get(self.url)  # переходим на тестируемый сайт
        # добавляем ожидание загрузки страницы сайта
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'signin-login')))
        except:
            self.logger.info('Ошибка при загрузке страницы при авторизации')
        # переводим форму в формат Sign in
        self.browser.execute_script("document.getElementsByClassName('fz-18')[3].click()")
        time.sleep(1)
        # получаем ссылки на поля формы для заполнения
        email_input = self.browser.find_element_by_id('signin-login')
        email_input.clear()
        password_input = self.browser.find_element_by_id('signin-pass')
        password_input.clear()
        # заполняем поля
        email_input.send_keys(login)
        password_input.send_keys(password)
        # нажимаем на элемент кнопки
        self.browser.find_element_by_xpath('//button[contains(text(), "Sign in")]').click()
        # ожидаем загрузку элемента с именем пользователя на главной странице
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "user-dropdown")))
            self.logger.info('Главная страница загружена успешно')
            return True
        except:
            self.logger.info("Ошибка при загрузке главной страницы после авторизации")
            return False

    def check_main_page(self):
        """
        Функция, проверяет основные элементы главной страницы сайта. Расширяется в зависимости от списка необходимых элементов.
        На текущий момент проверяется:
        - Имя пользователя;
        - Информация о подписке;
        - Ссылка на оплату тарифных планов;
        :return: status_dict - cловарь {Проверяемый элемент : статус элемента}
        """
        status_dict = {
            'Имя пользователя': {'status': False, 'details': None},
            'Подписка': {'status': False, 'details': None},
            'Plans': {'status': False, 'details': None}
        }
        # проверяем имя пользователя
        user_status, user_element = self.xpath_exists("//button[@id='user-dropdown']/span")
        status_dict['Имя пользователя']['status'] = user_status
        status_dict['Имя пользователя']['details'] = user_element.text

        # проверяем подписку
        plan_status, plan_element = self.xpath_exists("//div[@class='header-plan mr-32']")
        status_dict['Подписка']['status'] = plan_status
        status_dict['Подписка']['details'] = plan_element.text

        # проверяем ссылку на оплату тарифных планов
        pay_url_status, pay_url_element = self.xpath_exists("//a[contains(text(), 'Plans')]")
        status_dict['Plans']['status'] = pay_url_status
        status_dict['Plans']['details'] = pay_url_element.text

        return status_dict

    def check_pay_process(self):
        """
        Функция проверяет процесс оплаты по следующим шагам:
        1) Нажатие на ссылку "Plans" и переход на страницу выбора тарифного плана
        2) Нажатие кнопки "Select" под тарифным планом Base и переход на страницу оплаты
        3) Проверка перехода на сайт "store.payproglobal.com"
        :return: status_dict, где { Проверяемый параметр : статус проверки }
        """
        status_dict = {
            'Тарифный план': {'status': False, 'details': None},
            'Select': {'status': False, 'details': None},
            'Страница оплаты': {'status': False, 'details': None}
        }
        # ищем на странице ссылку Plans и нажимаем на нее с помощью JavaScript
        self.browser.execute_script('document.getElementsByClassName("dropdown-item")[0].click()')
        # ожидаем перехода на страницу с тарифными планами
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[@class="head-title mb-16"]')))
            self.logger.info('Страница с тарифными планами успешно загружена')
        except:
            self.logger.info("Ошибка при загрузке страницы с тарифными планами")
        # находим блок с базовым тарифным планом
        base_status, base_element = self.xpath_exists("//div[contains(text(), 'Base')]")
        status_dict['Тарифный план']['status'] = base_status
        # проверяем активность кнопки Select
        select_status, select_element = self.xpath_exists('//*[@id="panel"]/main/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]')
        status_dict['Select']['status'] = select_status
        # нажимаем на кнопку Select
        self.browser.execute_script('document.getElementsByClassName("plan-card__btn w-100-per")[0].click()')
        # ожидаем перехода на страницу оплаты
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "PayPro")]')))
            self.logger.info('Страница оплаты успешно загружена')
        except:
            self.logger.info("Ошибка при загрузке страницы оплаты")
        # проверяем совпадение домена страницы оплаты с необходимым
        if "store.payproglobal.com" in self.browser.current_url:
            status_dict['Страница оплаты']['status'] = True

        return status_dict
