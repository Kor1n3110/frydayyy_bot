# Импортируем необходимые классы.
from config import BOT_TOKEN
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from random import randint
from email.mime import application

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/genre', '/movie_details'],
                  ['/actors', '/favorites']]
keyboard_FLAG = False
genre_FLAG = False
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

genre_reply_keyboard = [['фентези', 'ужасы', 'драма'], ['детектив', 'приключения', 'комедия'],
                        ['боевик', 'биография', 'семейный'],
                        ['исторический', 'мультфильм'], ['СБРОС ПАРАМЕТРА', 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ', 'ВЫБРАЛ']]

genre_markup = ReplyKeyboardMarkup(genre_reply_keyboard, one_time_keyboard=False)

COMMAND = []
Genre = []
Movie_deteils = []
Actors = []
# *******
Genre1 = []
Movie_deteils1 = []
Actors1 = []
nasmeshka = ["Не понимаю, что вы выбрали, если вы ничего не выбрали... хотя ладно, мне никогда вас не понять",
             'Вы же ничего не выбрали...', 'Вы шутите так?', 'Я промолчу...']


# *******


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
    global COMMAND
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        'Укажите главных героев кино',
        reply_markup=ReplyKeyboardRemove()
    )
    COMMAND.append('Actors')


async def genre_command(update, context):
    global keyboard_FLAG, COMMAND, genre_FLAG
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        "Виберите жанры кино",
        reply_markup=genre_markup
    )
    COMMAND.append('Genre')
    # await update.message.reply_text(str(', '.join(COMMAND)))


async def movie_details_command(update, context):
    global COMMAND
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        'Заишите, что вы хотите видеть в кино',
        reply_markup=ReplyKeyboardRemove()
    )
    COMMAND.append('Movie_deteils')


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
    await update.message.reply_text(
        'Диалоговая клавиатура включена',
        reply_markup=markup
    )


async def close_keyboard(update, context):
    await update.message.reply_text(
        '',
        reply_markup=ReplyKeyboardRemove()
    )


async def MOGHO(update, context):
    global Genre, COMMAND, Movie_deteils, Actors, genre_FLAG, keyboard_FLAG, Genre1, Movie_deteils1, Actors1
    if update.message.text.upper() == 'ВЫБРАЛ':
        Genre = Genre1
        Movie_deteils = Movie_deteils1
        Actors = Actors1
        if COMMAND[-1] == 'Genre':
            if not Genre1 == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали жанр своего кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        elif COMMAND[-1] == 'Actors':
            if not Actors1 == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали актёров, ираюющих в вашем кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        else:
            if not Movie_deteils1 == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали детали вашего кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        if not Actors == []:
            a = str(', '.join(Actors))
        else:
            a = 'Не выбрал...'
        if not Genre == []:
            b = str(', '.join(Genre))
        else:
            b = 'Не выбрал...'
        if not Movie_deteils == []:
            c = str(', '.join(Movie_deteils))
        else:
            c = 'Не выбрал...'
        await update.message.reply_text(f'''Вы выбрали:
Актёры: {a}
Жанр: {b} 
Детали: {c}''')
    if COMMAND[-1] == 'Actors':
        if update.message.text not in Actors1 and not (
                update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
            Actors1.append(update.message.text)
            a = 'Вы выбрали: ' + ', '.join(Actors1)
            await update.message.reply_text(str(a))
        elif update.message.text in Actors1:
            await update.message.reply_text('Вы уже добавили этого актёра')
    elif COMMAND[-1] == 'Genre':
        if update.message.text not in Genre1 and not (
                update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
            Genre1.append(update.message.text)
            a = 'Вы выбрали: ' + ', '.join(Genre1)
            await update.message.reply_text(str(a))
        elif update.message.text in Genre1:
            await update.message.reply_text('Вы уже добавили этот жанр')
    else:
        if update.message.text not in Movie_deteils1 and not (
                update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
            Movie_deteils1.append(update.message.text)
            a = 'Вы выбрали: ' + ', '.join(Movie_deteils1)
            await update.message.reply_text(str(a))
        elif update.message.text in Movie_deteils1:
            await update.message.reply_text('Вы уже добавили эту деталь')
    if update.message.text.upper() == 'СБРОС ПАРАМЕТРА':
        if COMMAND[-1] == 'Genre':
            Genre = []
        elif COMMAND[-1] == 'Actors':
            Actors = []
        else:
            Movie_deteils = []
        await update.message.reply_text('Параметр сброшен')
    if update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ':
        if COMMAND[-1] == 'Genre':
            Genre1 = []
        elif COMMAND[-1] == 'Actors':
            Actors1 = []
        else:
            Movie_deteils1 = []
            await update.message.reply_text(
                "Вы вышли и сбросили параметр",
                reply_markup=markup
            )

    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    # -------------********************
    # await update.message.reply_text(update.message.text)
    # await update.message.reply_text(', '.join(COMMAND))
    # -------------********************


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
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, MOGHO)
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
