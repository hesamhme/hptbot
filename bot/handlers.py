from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from db.database import DatabaseManager
from db.models import SocialMediaType

db = DatabaseManager()

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("📱 Add Social Media", callback_data="add_social")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=reply_markup)


async def select_social_media(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(name, callback_data=f"social_{name}")] for name in SocialMediaType.__members__]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("🌐 Select a social media platform:", reply_markup=reply_markup)

async def get_username(update: Update, context: CallbackContext):

    query = update.callback_query
    social_media = query.data.split("_")[1]
    context.user_data["selected_social_media"] = social_media
    await query.message.reply_text(f"✍️ Enter your {social_media} username:")

async def save_username(update: Update, context: CallbackContext):

    telegram_id = update.message.from_user.id
    user_message = update.message.text.strip()
    social_media = context.user_data.get("selected_social_media")

    if social_media:
        db.add_user_profile(telegram_id, social_media, user_message)
        await update.message.reply_text(f"✅ Your username for {social_media} has been saved!")
    else:
        await update.message.reply_text("⚠️ Please select a social media platform first.")
