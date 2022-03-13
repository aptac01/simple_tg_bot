# -*- coding: utf-8 -*-
# та же фигня, как в main.py, но с записью простеньких данных в БД через sqlalchemy
# noinspection PyPackageRequirements
from telegram.ext import Updater, CommandHandler, CallbackContext
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import MessageHandler, Filters
from db import Database
from sqlalchemy import text


def make_db_query(query):
    """
    Открывает новый коннект, выполняет запрос и закрывает коннект
    """
    db = Database('localhost', 'tg_bot_password')
    db.init_engine()
    db_con = db.connection()
    result = None

    try:
        result = db_con.execute(text(query))
    except Exception as e:
        print(f'Возникла ошибка: {repr(e)}')
    finally:
        db.close_connection()

    return result


def save_user_to_db(update):
    """
    если пишет юзер в личку - сохраняем его в базу
    если он уже есть в базе - обновляем таймштамп
    """

    chat_id = update.effective_chat.id

    if update.effective_chat.type == 'private':
        select_res = make_db_query(f'select count(*) from USER_REQUESTS_STATS where USER_ID = \'{chat_id}\'')
        res = select_res.all()
        if res == [(1,)]:
            make_db_query(f'''UPDATE USER_REQUESTS_STATS SET DATE_OF=CURRENT_TIMESTAMP WHERE USER_ID='{chat_id}';''')
        else:
            make_db_query(f'''INSERT INTO USER_REQUESTS_STATS (USER_ID,DATE_OF) 
                    VALUES ('{chat_id}',CURRENT_TIMESTAMP);''')
    else:
        print('not a private chat, no updates were made to database')


def start(update: Update, context: CallbackContext):
    """
    Шлёт стартовое сообщение после команды /start
    """

    save_user_to_db(update)

    text = 'Здравствуйте! Вы позвонили на горячую линию ларька с шаурмой. Ваш звонок очень важен для вас. Вам ответит'\
           ' первый освободившийся Ашот. Пока можете посмотреть на меню:'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    with open('pic.jpg', 'rb') as pic_file:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic_file)


def echo(update: Update, context: CallbackContext):
    """
    Пример обработки сообщения пользователя
    """

    save_user_to_db(update)

    if update.message is not None:
        user_msg = update.message.text
        reply = f'> {user_msg}\nТебе сказали - жди? Вот и жди!'
    else:
        user_msg = update.edited_message.text
        reply = f'> {user_msg}\nТы чо йопта, думал я не замечу?'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


if __name__ == "__main__":

    # noinspection PyBroadException
    try:
        with open('config.txt', 'r') as file:
            token = file.read()
    except Exception:
        token = None

    if token in (None, ''):
        print('No bot token in config.txt file!')
        exit(1)

    updater = Updater(token=token)

    # хендлеры комманд (начинаются с /)
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    # хендлеры сообщений (просто текст)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(echo_handler)

    # стартуем
    updater.start_polling()
