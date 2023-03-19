# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from email.mime import application

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот 'Пятница'. Я помогу тебе выбрать кино и напомнить тебе о нём. Для начала напиши '/help'",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Сейчас объясню правила пользования мной.")
    await update.message.reply_text("Команда '/genre', даёт тебе возможность задать жанры кино")
    await update.message.reply_text(
        "С помощью команды '/movie_details', ты можешь уточнить, что ты хочешь видеть в кино (гонки, супергеоев и т.п.)")
    await update.message.reply_text("Написав '/actors', ты можешь указать главных героев в фильме")
    await update.message.reply_text("Воспользуясь командой '/remind', ты можешь поставить напоминание о кино")
    await update.message.reply_text("""Перейти в избранные - '/favorites',
Добавить в избранные - '/adding_favorites',
Удалить из избранных - '/delete_favorites'""")


async def actors_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Ты указываешь главных героев кино')


async def genre_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('Ты выбираешь жанр кино')


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


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text('Прости я пока ещё не готов...')


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("genre", genre_command))
    application.add_handler(CommandHandler("movie_details", movie_details_command))
    application.add_handler(CommandHandler("actors", actors_command))
    application.add_handler(CommandHandler("remind", remind_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("favorites", favorites_command))
    application.add_handler(CommandHandler("adding_favorites", adding_favorites_command))
    application.add_handler(CommandHandler("delete_favorites", delete_favorites_command))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
