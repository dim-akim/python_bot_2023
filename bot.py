from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove  # Обычная текстовая клавиатура
from telegram import InlineKeyboardButton, InlineKeyboardMarkup  # Инлайн-клавиатура
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters

import logging

from key import TOKEN

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
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
    inline_keyboard_handler = CommandHandler('inline_keyboard', do_inline_keyboard)
    set_timer_handler = CommandHandler('set', set_timer)
    callback_handler = CallbackQueryHandler(keyboard_react)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(set_timer_handler)
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
    text = [
        'Приветствую тебя, кожаный мешок!',
        f'Твой <b>{user_id=}</b>',
        'Я знаю команды:',
        '/start',
        '/keyboard',
        '/inline_keyboard',
        '/set',
        'html',
        '<b>Сам жирный</b>',
        '<i>Курсив</i>',
        '<code>код</code>',
        '<s>перечеркнутый</s>',
        '<u>подчеркнутый</u>',
        '<pre language="python">print("Hello, World!")</pre>',
        '<a href="https://technodzen.com/nauka/'
        'sozdan-magnitnyy-gel-zazhivlyayuschiy-rany-u-diabetikov-v-tri-raza-bystree?'
        'utm_source=yxnews&utm_medium=desktop">Сайт</a>'
    ]
    text = '\n'.join(text)
    # context.bot.send_message(
    #     user_id,
    #     text
    # )
    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


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


def do_inline_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_inline_keyboard')
    buttons = [
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['Погода в Москве']
    ]
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    logger.info(f'Создана клавиатура {keyboard}')
    text = 'Выбери одну из опций на клавиатуре'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info(f'Ответ улетел')


def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id
    logger.info(f'{user_id=} вызвал функцию keyboard_react')
    buttons = [
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['Погода в Москве']
    ]
    for row in buttons:
        if query.data in row:
            row.pop(row.index(query.data))
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Выбери другую опцию на клавиатуре'
    query.edit_message_text(
        text,
        reply_markup=keyboard
    )


def set_timer(update: Update, context: CallbackContext):
    context.job_queue.run_repeating(show_seconds, 10)


def show_seconds(context: CallbackContext):
    user_id = 262388958
    context.bot.send_message(user_id, 'прошло 10 секунд')


if __name__ == '__main__':
    main()
