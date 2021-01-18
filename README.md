# sl_web_testing_app

### Selenium-скрипт для тестирования формы авторизации и процесса оплаты тарифного плана

Файл запуска скрипта: **run.py**

Файл с классом Tester: **tester.py**

Папка с чек-листом и исходными данными для Selenium: **input_data/**

Папка с логами работы скрипта: **logs/**

Папка с результатами работы скрипта в формате Excel: **results/**

Папка с файлами chromedriver для разных ОС: **chromedriver/**
____________________

### Инструкция по запуску:

1) Клонировать репозиторий на локальный компьютер:
```
git clone https://github.com/Beumanc278/sl_web_testing_app.git
```
2) После загрузки репозитория через консоль перейти в папку скрипта и установить необходимые зависимости:
```
pip install -r requirements.txt
```
3) Добавить необходимый chromedriver в PATH (через командную строку или терминал):

  **Для Windows (запуск cmd от имени администратора):** 
  
    1) Сделать backup файла PATH ```echo %PATH% > C:\путь_до_папки_с_бекапом\path-backup.txt```
    
    2) Добавить путь к chromedriver в PATH ```setx path "%PATH%;C:\путь_до_проекта\sl_web_testing_app\chromedriver\Windows\" ```

  **Для Linux (проверено на Manjaro Linux):**
  
    1) В файл ~/.bashrc в конец добавить строку ``` export PATH="$HOME/путь_до_папки_проекта/sl_web_testing_app/chromedriver/Linux/:$PATH" ```
    2) Сохранить файл и загрузить новое значение в текущий сеанс оболочки ``` source ~/.bashrc ```
    
4) Для запуска скрипта использовать команду ``` python run.py ```
