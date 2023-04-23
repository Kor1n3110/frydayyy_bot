# Импортируем необходимые классы.
from config import BOT_TOKEN
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from random import randint
from random import choice
import sqlite3
import random
import requests
from telegram.ext import ApplicationBuilder

proxy_url = "socks5://user:pass@host:port"

app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()
from email.mime import application

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/genre', '/movie_details', '/actors'],
                  ['/facts', '/favorites', '/title'],
                  ['/GO']]
keyboard_FLAG = False
genre_FLAG = False
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

genre_reply_keyboard = [['фэнтези', 'ужасы', 'драма'], ['детектив', 'приключения', 'комедия'],
                        ['боевик', 'биография', 'семейный'],
                        ['исторический', 'мультфильм'], ['СБРОС ПАРАМЕТРА', 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ', 'ВЫБРАЛ']]

com_k = [['СБРОС ПАРАМЕТРА', 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ', 'ВЫБРАЛ']]
com_key = ReplyKeyboardMarkup(com_k, one_time_keyboard=False)


genre_markup = ReplyKeyboardMarkup(genre_reply_keyboard, one_time_keyboard=False)

nasmeshka = ["Не понимаю, что вы выбрали, если вы ничего не выбрали... хотя ладно, мне никогда вас не понять",
             'Вы же ничего не выбрали...', 'Вы шутите так?', 'Я промолчу...']


# *******


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    id_polz = user.mention_html()
    id_polz = id_polz.split('=')
    id_polz = str((''.join(id_polz[-1])).split('"')[0])
    id_polz = id_polz
    with open(f"{id_polz}_favorites.txt", "a"):
        pass
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот 'Пятница'. Я помогу тебе выбрать кино и напомнить тебе о нём. Для начала напиши '/help'.",
    )
    context.user_data['COMMAND'] = []
    context.user_data['Genre'] = []
    context.user_data['Genre1'] = []
    context.user_data['Actors'] = []
    context.user_data['Actors1'] = []
    context.user_data['Movie_deteils'] = []
    context.user_data['Movie_deteils1'] = []
    context.user_data['otvet'] = []
    print(context.user_data['COMMAND'])


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("""    Сейчас объясню правила пользования мной.

    Команда '/genre', даёт тебе возможность задать жанры кино.

    С помощью команды '/movie_details', ты можешь уточнить, что ты хочешь видеть в кино (гонки, супергеоев и т.п.).

    Написав '/actors', ты можешь указать актёров, игравших главные роли в фильме.

    Перейти в избранные - '/favorites',

    Добавить в избранные - '/adding_favorites',

    Удалить из избранных - '/delete_favorites'.

    Ты со мной можешь вести беседу через диалоговую клавиатуру, для её включения нужна команда '/keyboard', для выключения '/close_keyboard'.

    Так же я могу рссказать интересные факты о некоторых фильмах, для этого отправьте мне команду '/facts'

    Выбырай кино на свой вкус.""")
    await update.message.reply_text("""    Чтобы найти кино по названию, воспользуйтесь командой '/title'""")
    await update.message.reply_text(
        "    Чтобы начать поиск кино, воспользуйтесь командой '/GO'",
        reply_markup=markup
    )


async def actors_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        'Укажите главных героев кино',
        reply_markup=com_key
    )
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['Actors']


async def genre_command(update, context):
    global keyboard_FLAG, COMMAND, genre_FLAG
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        "Виберите жанры кино",
        reply_markup=genre_markup
    )
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['Genre']


async def movie_details_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        'Заишите, что вы хотите видеть в кино',
        reply_markup=com_key
    )
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['Movie_deteils']


async def remind_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('хорошо, напомню!🫡')


async def favorites_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Секундочку🤔‍')
    user = update.effective_user
    id_polz = user.mention_html()
    id_polz = id_polz.split('=')
    id_polz = str((''.join(id_polz[-1])).split('"')[0])
    id_polz = id_polz
    with open(f'{id_polz}_favorites.txt', 'r') as fp:
        sp = fp.readlines()
    if not sp == []:
        for i in sp:
            Id = i[:-1]
            con = sqlite3.connect("cinema.db")
            # Создание курсора
            cur = con.cursor()
            # Выполнение запроса и получение всех результатов
            result = cur.execute(f"""SELECT name FROM cinema_baza_dan WHERE id = {Id}""")
            three_results = cur.fetchmany(210)
            for u in three_results:
                for y in u:
                    if y[-1] == ' ':
                        y = y[:-1]
                    await update.message.reply_text(f'id: {Id} - "{y}"')
    else:
        await update.message.reply_text(f'В избранный ничего нет😅')


async def adding_favorites_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Пришли мне id кино, которого хотите добавить в "избранные"')
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['A_F']


async def delete_favorites_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Пришли мне id кино, которого хотите удалить из "избранные"')
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['D_F']


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


async def GO(update, context):
    if not context.user_data['Actors'] == []:
        a = str(', '.join(context.user_data['Actors']))
    else:
        a = 'Не выбрали...'
    if not context.user_data['Genre'] == []:
        b = str(', '.join(context.user_data['Genre']))
        print(b)
    else:
        b = 'Не выбрали...'
    if not context.user_data['Movie_deteils'] == []:
        c = str(', '.join(context.user_data['Movie_deteils']))
    else:
        c = 'Не выбрали...'
    await update.message.reply_text(f'''Вы выбрали:
Актёры: {a}
Жанр: {b}
Детали: {c}''')
    await update.message.reply_text('Так, а сейчас будем искать кино по вашим интересам)')
    con = sqlite3.connect("cinema.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""SELECT * FROM cinema_baza_dan""")
    three_results = cur.fetchmany(210)
    for u in three_results:
        print(len(context.user_data['Genre']))
        if len(context.user_data['Genre']) > 0 and len(context.user_data['Movie_deteils']) > 0:
            for i in context.user_data['Genre']:
                if i in u[4] and i not in context.user_data['otvet']:
                    for y in context.user_data['Movie_deteils']:
                        if y in u[5] and y not in context.user_data['otvet']:
                            context.user_data['otvet'] = context.user_data['otvet'] + [u]
        elif len(context.user_data['Genre']) == 0 and len(context.user_data['Movie_deteils']) > 0:
            if len(context.user_data['Movie_deteils']) > 0:
                for y in context.user_data['Movie_deteils']:
                    if y in u[5] and y not in context.user_data['otvet']:
                        context.user_data['otvet'] = context.user_data['otvet'] + [u]
        elif len(context.user_data['Genre']) > 0 and len(context.user_data['Movie_deteils']) == 0:
            if len(context.user_data['Genre']) > 0:
                for y in context.user_data['Genre']:
                    if y in u[5] and y not in context.user_data['otvet']:
                        context.user_data['otvet'] = context.user_data['otvet'] + [u]
        if len(context.user_data['Actors']) > 0:
            for i in context.user_data['Actors']:
                if i in u[7] and i not in context.user_data['otvet']:
                    context.user_data['otvet'] = context.user_data['otvet'] + [u]
    if not context.user_data['otvet'] == []:
        await update.message.reply_text('Мы нашли названия фильмов, которые подойдут вам')
        await update.message.reply_text('😊')
        for o in context.user_data['otvet']:
            await update.message.reply_text(str(o[1]))
        await update.message.reply_text('Посмотреть более точную информацию можно с помощью команды /title')
    context.user_data['COMMAND'] = []
    context.user_data['Genre'] = []
    context.user_data['Genre1'] = []
    context.user_data['Actors'] = []
    context.user_data['Actors1'] = []
    context.user_data['Movie_deteils'] = []
    context.user_data['otvet'] = []
    context.user_data['Movie_deteils1'] = []


async def facts(update, contex):
    await update.message.reply_text('А вы знали?🤔')
    with open('facts.txt', 'r', encoding="utf8") as fp:
        sp = fp.readlines()
    await update.message.reply_text(str(choice(sp)))


async def title(update, context):
    context.user_data['COMMAND'] = context.user_data['COMMAND'] + ['Title']
    await update.message.reply_text('Отправьте мне название кино, и если я его найду, то пришлю всё что о нём узнаю😊')


async def MOGHO(update, context):
    if context.user_data['COMMAND'][-1] == 'Title':
        name = str(update.message.text)
        cinema_po_nazvaniy = []
        # Подключение к БД
        con = sqlite3.connect("cinema.db")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute(f"""SELECT * FROM cinema_baza_dan""")
        three_results = cur.fetchmany(210)
        for i in three_results:
            if str(i[1]).lower().split() == name.lower().split():
                cinema_po_nazvaniy = i
                break
        if cinema_po_nazvaniy == []:
            await update.message.reply_text('Извините, я не нашёл это кино😓')
        else:
            await update.message.reply_text('НАШЁЛ!')
            await update.message.reply_text(f'''id: {cinema_po_nazvaniy[0]}

Название: {str(cinema_po_nazvaniy[1])}

Тип: {str(cinema_po_nazvaniy[2].lower())}

Год выпуска: {str(cinema_po_nazvaniy[3])}

Жанр: {str(cinema_po_nazvaniy[4])}

Описание {str(cinema_po_nazvaniy[2].lower())}а: {str(cinema_po_nazvaniy[6])}

Актёры: {str(cinema_po_nazvaniy[7])}

Ссылка на трейлер: {str(cinema_po_nazvaniy[8])}

Ссылка на {str(cinema_po_nazvaniy[2].lower())}: {str(cinema_po_nazvaniy[9])}''')
    if context.user_data['COMMAND'][-1] == 'A_F':
        ID = int(update.message.text)
        if ID >= 1 and ID <= 210:
            ID = str(ID)
            user = update.effective_user
            id_polz = user.mention_html()
            id_polz = id_polz.split('=')
            id_polz = str((''.join(id_polz[-1])).split('"')[0])
            id_polz = id_polz
            with open(f'{id_polz}_favorites.txt', 'r') as fp:
                sp = fp.readlines()
            if str(ID) + '\n' not in sp:
                sp.append(str(ID) + '\n')
                user = update.effective_user
                with open(f'{id_polz}_favorites.txt', 'w') as fp:
                    for i in sp:
                        sps = fp.write(i)
                await update.message.reply_text(
                    f"Добавил кино с id {str(ID)} в избранные. Чтобы посмотреть избранные, воспользуйтесь команой '/favorites'")
            else:
                await update.message.reply_text(
                    f"Кино с id {str(ID)} уже добавлено в избранные. Чтобы посмотреть избранные, воспользуйтесь команой '/favorites'")
        else:
            await update.message.reply_text('НЕВЕЕРНЫЙ ID😡')
    if context.user_data['COMMAND'][-1] == 'D_F':
        context.user_data['SPISOK_NEW'] = []
        ID_D = int(update.message.text)
        if ID_D >= 1 and ID_D <= 210:
            user = update.effective_user
            id_polz = user.mention_html()
            id_polz = id_polz.split('=')
            id_polz = str((''.join(id_polz[-1])).split('"')[0])
            id_polz = id_polz
            with open(f'{id_polz}_favorites.txt', 'r') as fp:
                sp = fp.readlines()
            if str(ID_D) + '\n' in sp:
                for i in sp:
                    if not int(i[:-1]) == ID_D:
                        context.user_data['SPISOK_NEW'] = context.user_data['SPISOK_NEW'] + [i]
                user = update.effective_user
                with open(f'{id_polz}_favorites.txt', 'w') as fp:
                    for i in context.user_data['SPISOK_NEW']:
                        sps = fp.write(i)
                await update.message.reply_text(
                    f"Удалил кино с id {str(ID_D)} из избранных. Чтобы посмотреть избранные, воспользуйтесь команой '/favorites'")
            else:
                await update.message.reply_text(
                    f"Кино с id {str(ID_D)} не найдено в избранный. Чтобы посмотреть избранные, воспользуйтесь команой '/favorites'")
        else:
            await update.message.reply_text('НЕВЕЕРНЫЙ ID😡')

    if update.message.text.upper() == 'ВЫБРАЛ':
        context.user_data['Genre'] = context.user_data['Genre1']
        context.user_data['Movie_deteils'] = context.user_data['Movie_deteils1']
        context.user_data['Actors'] = context.user_data['Actors1']
        if context.user_data['COMMAND'][-1] == 'Genre':
            if not context.user_data['Genre1'] == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали жанр своего кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        elif context.user_data['COMMAND'][-1] == 'Actors':
            if not context.user_data['Actors1'] == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали актёров, играющих в вашем кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        else:
            if not context.user_data['Movie_deteils1'] == []:
                await update.message.reply_text(
                    "Замечательно, вы выбрали детали вашего кино.",
                    reply_markup=markup
                )
            else:
                await update.message.reply_text(
                    nasmeshka[randint(0, 3)],
                    reply_markup=markup
                )
        if not context.user_data['Actors'] == []:
            a = str(', '.join(context.user_data['Actors']))
        else:
            a = 'Не выбрал...'
        if not context.user_data['Genre'] == []:
            b = str(', '.join(context.user_data['Genre']))
        else:
            b = 'Не выбрал...'
        if not context.user_data['Movie_deteils'] == []:
            c = str(', '.join(context.user_data['Movie_deteils']))
        else:
            c = 'Не выбрал...'
        await update.message.reply_text(f'''Вы выбрали:
Актёры: {a}
Жанр: {b} 
Детали: {c}''')
    if not context.user_data['COMMAND'][-1] == 'Title' and not context.user_data['COMMAND'][-1] == 'A_F' and not \
            context.user_data['COMMAND'][-1] == 'D_F':
        if context.user_data['COMMAND'][-1] == 'Actors':
            if update.message.text not in context.user_data['Actors1'] and not (
                    update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
                context.user_data['Actors1'] += [update.message.text]
                a = 'Вы выбрали: ' + ', '.join(context.user_data['Actors1'])
                await update.message.reply_text(str(a))
            elif update.message.text in context.user_data['Actors1']:
                await update.message.reply_text('Вы уже добавили этого актёра')
        elif context.user_data['COMMAND'][-1] == 'Genre':
            print(context.user_data['COMMAND'])
            if update.message.text not in context.user_data['Genre1'] and not (
                    update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
                context.user_data['Genre1'] += [update.message.text]
                print(context.user_data['Genre1'])
                a = 'Вы выбрали: ' + ', '.join(context.user_data['Genre1'])
                await update.message.reply_text(str(a))
            elif update.message.text in context.user_data['Genre1']:
                await update.message.reply_text('Вы уже добавили этот жанр')
        else:
            if update.message.text.lower() not in context.user_data['Movie_deteils1'] and not (
                    update.message.text.upper() == 'ВЫБРАЛ' or update.message.text.upper() == 'СБРОС ПАРАМЕТРА' or update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ'):
                context.user_data['Movie_deteils1'] += [update.message.text.lower()]
                a = 'Вы выбрали: ' + ', '.join(context.user_data['Movie_deteils1'])
                await update.message.reply_text(str(a))
            elif update.message.text in context.user_data['Movie_deteils1']:
                await update.message.reply_text('Вы уже добавили эту деталь')
        if update.message.text.upper() == 'СБРОС ПАРАМЕТРА':
            if context.user_data['COMMAND'][-1] == 'Genre':
                context.user_data['Genre'] = []
            elif context.user_data['COMMAND'][-1] == 'Actors':
                context.user_data['Actors'] = []
            else:
                context.user_data['Movie_deteils'] = []
            await update.message.reply_text('Параметр сброшен')
        if update.message.text.upper() == 'СБРОСИТЬ ПАРАМЕТР И ВЫЙТИ':
            if context.user_data['COMMAND'][-1] == 'Genre':
                context.user_data['Genre1'] = []
            elif context.user_data['COMMAND'][-1] == 'Actors':
                context.user_data['Actors1'] = []
            else:
                context.user_data['Movie_deteils1'] = []
                await update.message.reply_text(
                    "Вы вышли и сбросили параметр",
                    reply_markup=markup
                )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
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
    application.add_handler(CommandHandler("GO", GO))
    application.add_handler(CommandHandler('title', title))
    application.add_handler(CommandHandler("facts", facts))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, MOGHO)
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
