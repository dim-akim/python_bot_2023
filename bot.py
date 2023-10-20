from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters

import logging

from key import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    # Объект, который вытягивает обновления из Telegram
    updater = Updater(token=TOKEN)

    # Диспетчер будет распределять обновления по обработчикам
    dispatcher: Dispatcher = updater.dispatcher

    # Создаем обработчик, который все текстовые сообщения переправляет в функцию do_echo
    echo_handler = MessageHandler(Filters.text, do_echo)
    start_handler = CommandHandler(['start', 'help'], do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def do_echo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text

    logger.info(f'{username=} {user_id=} вызвал функцию echo')
    answer = [
        f'Твой {user_id=}',
        f'Твой {username=}',
        f'Ты написал {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())


def do_start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию start')
    text = ['Приветствую тебя, кожаный мешок!',
            f'Твой {user_id=}',
            'Я знаю команды:',
            '/start',
            '/keyboard'
    ]
    text = '\n'.join(text)
    # context.bot.send_message(
    #     user_id,
    #     text
    # )
    update.message.reply_text(text)


def do_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_keyboard')
    buttons = [  # 3 ряда кнопок
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['Погода в Москве']
    ]
    logger.info(f'Созданы кнопки {buttons}')
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    logger.info(f'Создана клавиатура {keyboard}')
    text = 'Выбери одну из опций на клавиатуре'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info(f'Ответ улетел')


if __name__ == '__main__':
    main()
