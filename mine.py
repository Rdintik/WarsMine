import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Считываем токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("Нет переменной TELEGRAM_TOKEN. Проверьте .env или настройки хостинга.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Я тут!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
