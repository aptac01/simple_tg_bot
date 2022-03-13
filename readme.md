## simple_tg_bot

Телеграм-бот с базовыми реакциями на юзера на основе PTB (https://github.com/python-telegram-bot/python-telegram-bot)

Для запуска нужен установленный в системе python 3.6.8+, я использовал 3.8.10, далее:

```
python3 -m venv env
./env/bin/python -m pip install -r requirements.txt 
```

Для запуска:
```
./env/bin/python main.py
```

Для использования нужно создать бота через bot_father'а, токен поместить в файл config.txt

Для использования main_db.py нужна развернутая и запущенная БД firebird (v2.5, другие версии не тестировал)