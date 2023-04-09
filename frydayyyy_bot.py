# Импортируем необходимые классы.
from config import BOT_TOKEN
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from email.mime import application

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/genre'], ['/movie_details'],
                  ['/actors'], ['/favorites']]
keyboard_FLAG = False
genre_FLAG = False
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

genre_reply_keyboard = [['фентези', 'ужасы', 'драма'], ['детектив', 'приключения', 'комедия'],
                        ['боевик', 'биография', 'семейный'],
                        ['исторический', 'мультфильм'], ['НАЗАД', 'ВЫБРАЛ']]

genre_markup = ReplyKeyboardMarkup(genre_reply_keyboard, one_time_keyboard=False)

Genre = []
Movie_deteils = []
Actors = []


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот 'Пятница'. Я помогу тебе выбрать кино и напомнить тебе о нём. Для начала напиши '/help'.",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("""    Сейчас объясню правила пользования мной.
    Команда '/genre', даёт тебе возможность задать жанры кино.
    С помощью команды '/movie_details', ты можешь уточнить, что ты хочешь видеть в кино (гонки, супергеоев и т.п.).
    Написав '/actors', ты можешь указать актёров, игравшие главные роли в фильме.
    Воспользуясь командой '/remind', ты можешь поставить напоминание о кино.
    Перейти в избранные - '/favorites',
    Добавить в избранные - '/adding_favorites',
    Удалить из избранных - '/delete_favorites'.
    Ты со мной можешь вести беседу через диалоговую клавиатуру, для её включения нужна команда '/keyboard', для выключения '/close_keyboard'.
    Выбырай кино на свой вкус.""")


async def actors_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Ты указываешь главных героев кино')


async def genre_command(update, context):
    global keyboard_FLAG
    """Отправляет сообщение когда получена команда /help"""
    if keyboard_FLAG is True:
        await update.message.reply_text(
            "Диалоговая клавиатура выключена",
            reply_markup=ReplyKeyboardRemove()
        )
        keyboard_FLAG = False
    await update.message.reply_text(
        "Виберите жанры кино",
        reply_markup=genre_markup
    )


async def movie_details_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Пишешь, что ты хочешь видеть в кино')


async def remind_command(update, contex):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('хорошо, напомню!🫡')


async def favorites_command(update, contex):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('В избранных ничего нет')


async def adding_favorites_command(update, contex):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Я добавлю, когда буду готов...')


async def delete_favorites_command(update, contex):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Я удалю, когда буду готов...')


async def keyboard(update, context):
    global genre_FLAG, keyboard_FLAG
    if genre_FLAG is True:
        await update.message.reply_text(
            "Диалоговая клавиатура выключена",
            reply_markup=ReplyKeyboardRemove()
        )
        genre_FLAG = False
    await update.message.reply_text(
        "Диалоговая клавиатура включена",
        reply_markup=markup
    )
    keyboard_FLAG = True


async def close_keyboard(update, context):
    global keyboard_FLAG
    await update.message.reply_text(
        "Диалоговая клавиатура выключена",
        reply_markup=ReplyKeyboardRemove()
    )
    keyboard_FLAG = False


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("genre", genre_command))
    application.add_handler(CommandHandler("movie_details", movie_details_command))
    application.add_handler(CommandHandler("actors", actors_command))
    application.add_handler(CommandHandler("remind", remind_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("favorites", favorites_command))
    application.add_handler(CommandHandler("adding_favorites", adding_favorites_command))
    application.add_handler(CommandHandler("delete_favorites", delete_favorites_command))
    application.add_handler(CommandHandler("keyboard", keyboard))
    application.add_handler(CommandHandler("close_keyboard", close_keyboard))
    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
