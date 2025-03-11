from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, filters
from db.database import DatabaseManager
from db.models import SocialMediaType
from db.fake_db import fake_db  # Ensure correct import
import random

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
    context.user_data["state"] = "waiting_for_username" 
    await query.message.reply_text(f"✍️ Enter your {social_media} username:")

async def save_username(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    username = update.message.text.strip()
    social_media = context.user_data.get("selected_social_media")

    if social_media:
        db.add_user_profile(telegram_id, social_media, username)
        if username not in fake_db:
            fake_db[username] = {
                "followers_count": random.randint(500, 5000),
                "target": None
            }
        
        keyboard = [
            [InlineKeyboardButton("👥 Check Followers", callback_data=f"check_followers_{username}")],
            [InlineKeyboardButton("🔔 Set Alert", callback_data=f"set_alert_{username}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"✅ Your username for {social_media} has been saved!\nChoose an option:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("⚠️ Please select a social media platform first.")

async def check_followers(update: Update, context: CallbackContext):
    query = update.callback_query
    username = query.data.split("_")[2]

    if username in fake_db:
        count = fake_db[username]["followers_count"]
        keyboard = [
            [InlineKeyboardButton("👥 Check Followers", callback_data=f"check_followers_{username}")],
            [InlineKeyboardButton("🔔 Set Alert", callback_data=f"set_alert_{username}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"👥 {username} has {count} followers.", reply_markup=reply_markup)
    else:
        await query.message.reply_text("⚠️ User not found.")

async def set_alert(update: Update, context: CallbackContext):
    query = update.callback_query
    username = query.data.split("_")[2]
    context.user_data["pending_alert"] = username
    context.user_data["state"] = "waiting_for_alert"
    await query.message.reply_text("🔔 Enter the number of followers to set an alert:")

async def save_alert(update: Update, context: CallbackContext):
    username = context.user_data.get("pending_alert")
    if not username:
        await update.message.reply_text("⚠️ No username selected.")
        return

    try:
        target = int(update.message.text.strip())
        if username in fake_db:
            fake_db[username]["target"] = target
            
            keyboard = [
                [InlineKeyboardButton("👥 Check Followers", callback_data=f"check_followers_{username}")],
                [InlineKeyboardButton("🔔 Set Alert", callback_data=f"set_alert_{username}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"✅ Alert for {username} has been set at {target} followers!",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("⚠️ User not found.")
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number.")

    context.user_data.pop("pending_alert", None)
    context.user_data.pop("state", None)

async def handle_text_input(update: Update, context: CallbackContext):
    state = context.user_data.get("state")

    if state == "waiting_for_username":
        await save_username(update, context)
    elif state == "waiting_for_alert":
        await save_alert(update, context)
    else:
        await update.message.reply_text("⚠️ Invalid input.")