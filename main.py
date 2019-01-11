# -*- coding: utf-8 -*-

import requests

import logging
from config import tokenAPI

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

NEW, LOGIN, PASSWORD = range(3)

status = dict()

data = dict()


def delete_user(bot, update):
    # Получаем чат ID
    chat_id = update.message.chat.id
    # Получаем ID юзера
    user_id = update.message.from_user.id

    headers = {'content-type': 'application/json', 'charset': 'UTF-8'}

    delete_user = requests.delete('https://service.modulpos.ru/api/v1/user', headers=headers,
                                  auth=(data[user_id]['login'], data[user_id]['password']))
    if delete_user.status_code == 200:
        bot.sendMessage(chat_id, text='Юзер успешно удален')
    else:
        bot.sendMessage(chat_id, text='Произошла ошибка, код - ' + str(delete_user.status_code))


def talk(bot, update):
    # Получаем чат ID
    chat_id = update.message.chat.id
    # Получаем ID юзера
    user_id = update.message.from_user.id
    # Получаем сообщение от юзера
    message = update.message.text

    # Проверяем статус действия
    state = status.get(user_id, NEW)

    # Проверяем от кого сообщение (бот или юзер)
    if not update.message.from_user.is_bot:
        # Проверяем соответствует ли статус
        if state == NEW:
            data[user_id] = {}
            # Выводим сообщение
            bot.sendMessage(chat_id, text='Введите Email юзера:')
            # Меняем статус
            status[user_id] = LOGIN
        elif state == LOGIN:
            # Добавляем логин
            data[user_id].update({'login': message})
            # Выводим сообщение
            bot.sendMessage(chat_id, text='Введите пароль юзера:')
            # Меняем статус
            status[user_id] = PASSWORD
        elif state == PASSWORD:
            data[user_id].update({'password': message})
            delete_user(bot, update)


def start(bot, update):
    # Получаем чат ID
    chat_id = update.message.chat.id
    # Получаем ID юзера
    user_id = update.message.from_user.id

    bot.sendMessage(chat_id, text='Приветствую. Введи любое сообщение для начала работы.')


def main():
    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    updater = Updater(tokenAPI)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(Filters.text, talk))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
