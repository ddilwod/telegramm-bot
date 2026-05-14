import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === SOZLAMALAR ===
TOKEN = "8890689359:AAF6l6smPZvpyvD7mc0dmENkj3BZeGxxm40"
KANAL = "@davronov_uzum_service"
# ==================

logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(KANAL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Obuna tekshirishda xato: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id
    msg = update.message

    is_subscribed = await check_subscription(user_id, context)

    if not is_subscribed:
        keyboard = [[InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/davronov_uzum_service")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.reply_text(
            "❌ Botdan foydalanish uchun avval kanalga obuna bo'ling!\n\n"
            "✅ Obuna bo'lgach, faylni qayta yuboring.",
            reply_markup=reply_markup
        )
        return

    if msg.document:
        await msg.reply_document(msg.document.file_id, caption="✅ Mana faylingiz!")
    elif msg.photo:
        await msg.reply_photo(msg.photo[-1].file_id, caption="✅ Mana rasmingiz!")
    elif msg.video:
        await msg.reply_video(msg.video.file_id, caption="✅ Mana videongiz!")
    elif msg.audio:
        await msg.reply_audio(msg.audio.file_id, caption="✅ Mana audiongiz!")
    elif msg.text:
        await msg.reply_text("✅ Xabaringiz qabul qilindi!")
    else:
        await msg.reply_text("✅ Fayl qabul qilindi!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
