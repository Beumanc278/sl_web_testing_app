import os
from tester import Tester
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import logging

def write_results(data, check_id, status_dict):
    """
    Функция проверяет результаты работы Tester'a и в зависимости от них проставляет статусы проверок
    в исходный датафрейм
    :param data: датафрейм с данными из чек-листа
    :param check_id: id, который проверяется на текущий момент
    :param status_dict: результат работы Tester'a в виде dict
    :return: data: датафрейм с актуальным статусом проверки
    """
    # проверяем пройден ли тест, в зависимости от Проверяемого параметра
    check_index = data[data['ID'] == check_id].index[0]
    check_parameter = data[data['ID'] == check_id]['Проверяемый параметр'].values[0]
    check_status = data[data['ID'] == check_id]['Ожидаемое состояние'].values[0]
    try:
        if status_dict[check_parameter]['status'] == check_status:
            data.loc[check_index, 'Статус проверки Selenium'] = 'Passed'
        elif status_dict[check_parameter]['status'] != check_status:
            data.loc[check_index, 'Статус проверки Selenium'] = 'Failed'
        else:
            logger.info(f'Не удалось определить Статус проверки Selenium в ходе проверки ID = {check_id}')
        return data
    except Exception as ex:
        logger.info(f'Возникла ошибка при проверке ID = {check_id}')
        return data

if __name__ == "__main__":
    
    # запускаем логгирование в консоли
    logger = logging.getLogger()
    logger.info('Скрипт запущен...')
    
    # инициализируем класс
    tester = Tester()
    logger.info('Инициализирован класс Tester...')
    
    # загружаем в датафрейм чек-лист и исходные данные для проверки
    data = pd.read_excel(os.path.abspath(os.curdir) + '\\input_data\\Чек-лист.xlsx', engine='openpyxl')
    logger.info(f'Загружены данные проверок из чек-листа...')
    
    # фиксируем ссылку на тестируемый сайт и передаем в tester
    test_url = 'https://area-dev.sl-int.team.'
    tester.set_test_url(test_url)

    # из всего датафрейма выбираю только строки с объектом тестирования = "Форма авторизации"
    check_data = data[data['Объект тестирования'] == 'Форма авторизации']
    # по ID обращаемся к каждой строке проверки
    logger.info("Запускаем проверки для объекта - Форма авторизации")
    for check_id in tqdm(check_data['ID']):
        # извлекаем логин и пароль для выбранной проверки
        test_login = data[data['ID'] == check_id]['Логин'].values[0]
        test_password = data[data['ID'] == check_id]['Пароль'].values[0]
        # проводим авторизацию по выбранным логину и паролю и получаем статусы параметров
        status_dict = tester.authorization_test(check_id, test_login, test_password)
        # заводим итоги проверки в датафрейм
        data = write_results(data, check_id, status_dict)

    success_id = 5 # задаем id успешной проверки с корректными данными для входа
    # проверяем, пройдена ли проверка на успешную авторизацию
    if data[data['ID'] == success_id]['Статус проверки Selenium'].values[0] == 'Passed':
        success_login = data[data['ID'] == success_id]['Логин'].values[0]
        success_password = data[data['ID'] == success_id]['Пароль'].values[0]
        main_page = tester.authorize(success_login, success_password)
        # если главная страница загружена успешно
        if main_page:
            # проверяем наличие основных элементов на Главной странице сайта
            check_data = data[data['Объект тестирования'] == 'Главная страница сайта']
            logger.info("Запускаем проверки для объекта - Главная страница сайта")
            status_dict = tester.check_main_page()
            for check_id in tqdm(check_data['ID']):
                # заводим итоги проверки в датафрейм
                data = write_results(data, check_id, status_dict)
            # проверяем процедуру оплаты
            check_data = data[data['Объект тестирования'] == 'Оплата тарифного плана']
            logger.info('Запускаем проверки для объекта - Оплата тарифного плана')
            # получаем статусы со всех этапов процедуры
            status_dict = tester.check_pay_process()
            for check_id in tqdm(check_data['ID']):
                data = write_results(data, check_id, status_dict)

    # создаем файл Excel в папке ./results для сохранения результатов
    result_filename = f'result - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
    result_savepath = os.path.abspath(os.curdir) + '\\results\\' + result_filename
    # сохраняем книгу Excel с результатами
    data.to_excel(result_savepath)
    logger.info(f'Файл с результатами проверок сохранен в {result_savepath}')
    # завершаем работу web-драйвера
    tester.close_webdriver()
    logger.info('Завершена работа Tester')