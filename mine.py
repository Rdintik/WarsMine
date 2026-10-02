import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, InlineQueryHandler, CommandHandler, ContextTypes

# Включаем логирование для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обработчик команды /start (чтобы бот не молчал при прямом обращении)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот-в-боте.\n"
        "Напиши в любом чате @username_вашего_бота и выбери результат, чтобы увидеть свой юзернейм."
    )

# Главный обработчик Inline-запросов
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    # Создаем результат, который увидит пользователь в окошке
    # Мы используем uuid4(), чтобы у каждого результата был уникальный ID
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Показать мой юзернейм",
            description="Нажми, чтобы бот написал твой @username",
            # Это сообщение придет в чат после клика
            input_message_content=InputTextMessageContent(
                "Я пока не знаю твой юзернейм, нажми на меня!"
            )
        )
    ]

    # Отвечаем на запрос, показывая окошко
    await update.inline_query.answer(results)

# Обработчик нажатия на результат (Callback Query)
# Именно здесь мы узнаем, КТО нажал на кнопку/результат
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Обязательно нужно подтвердить получение нажатия

    # Получаем данные пользователя, который нажал
    user = query.from_user
    
    # Формируем текст. Если юзернейма нет, пишем имя
    if user.username:
        text = f"Твой юзернейм: @{user.username}"
    else:
        text = f"У тебя нет юзернейма. Твое имя: {user.first_name}"

    # Редактируем сообщение, которое бот прислал после клика
    await query.edit_message_text(text=text)

def main() -> None:
    # ВАЖНО: Токен лучше брать из переменных окружения (os.getenv), 
    # но для теста можно вписать сюда строку
    TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

    app = Application.
