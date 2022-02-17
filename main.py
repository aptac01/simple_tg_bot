# -*- coding: utf-8 -*-
# пакет называется python-telegram-bot, но Python-модуль почему-то просто telegram ¯\_(ツ)_/¯
# noinspection PyPackageRequirements
from telegram.ext import Updater, CommandHandler, CallbackContext
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import MessageHandler, Filters


def start(update: Update, context: CallbackContext):
    """
    Шлёт стартовое сообщение после команды /start
    """
    text = 'Здравствуйте! Вы позвонили на горячую линию ларька с шаурмой. Ваш звонок очень важен для вас. Вам ответит'\
           ' первый освободившийся Ашот. Пока можете посмотреть на меню:'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    pic_file = open('pic.jpg', 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic_file)
    pic_file.close()


def echo(update: Update, context: CallbackContext):
    """
    Пример обработки сообщения пользователя
    """
    if update.message is not None:
        user_msg = update.message.text
        reply = f'> {user_msg}\nВай! Зачэм ругаэщся! Не ругайса, ну?!'
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
