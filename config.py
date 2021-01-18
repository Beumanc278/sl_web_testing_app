import os
from datetime import datetime

"""
Файл содержит настройки для скрипта
1) Путь к chromedriver (выбирается в зависимости от системы, на которой используется)
2) Ссылка на тестируемый веб-сайт
3) Папка с логами и имя файла логов
4) Папка для сохранения результатов
5) Папка с чек-листом и исходными данными для скрипта
"""

# задаем путь к chromedriver (изменить в зависимости от используемой системы)
driver_path = os.path.abspath(os.curdir) + "\\chromedriver\\Windows\\chromedriver.exe"

# задаем ссылку на тестируемый сайт
test_url = 'https://area-dev.sl-int.team.'

# задаем папку с логами и название файла с логами
logfile_name = f'.\logs\log - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log'

# задаем путь к файлу для сохранения результатов
result_filename = f'result - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
result_savepath = os.path.abspath(os.curdir) + '\\results\\' + result_filename

# задаем путь к файлу с чек-листом и исходными данными для скрипта
input_data = os.path.abspath(os.curdir) + '\\input_data\\Чек-лист.xlsx'