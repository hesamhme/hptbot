import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers import start, select_social_media, get_username, save_username, check_followers, set_alert, save_alert, handle_text_input

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

t_app = ApplicationBuilder().token(BOT_TOKEN).build()

t_app.add_handler(CommandHandler("start", start))
t_app.add_handler(CallbackQueryHandler(select_social_media, pattern="^add_social$"))
t_app.add_handler(CallbackQueryHandler(get_username, pattern="^social_\\w+$"))
t_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
t_app.add_handler(CallbackQueryHandler(check_followers, pattern="^check_followers_\\w+$"))
t_app.add_handler(CallbackQueryHandler(set_alert, pattern="^set_alert_\\w+$"))

def start_bot():
    logger.info("🤖 Bot is running...")
    t_app.run_polling()

if __name__ == "__main__":
    start_bot()
