import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
)
from bot.handlers import start, select_social_media, get_username, save_username       

# env setting
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# log setting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_social_media, pattern="^add_social$"))
    app.add_handler(CallbackQueryHandler(get_username, pattern="^social_\\w+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_username))
    
    logger.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
