import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8890689359:AAF6l6smPZvpyvD7mc0dmENkj3BZeGxxm40"
KANAL = "@davronov_uzum_service"

logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id, bot):
    try:
        member = await bot.get_chat_member(KANAL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Xato: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.effective_user.id
    msg = update.message
    is_sub = await check_subscription(user_id, context.bot)
    if not is_sub:
        kb = [[InlineKeyboardButton("📢 Obuna bo'lish", url="https://t.me/davronov_uzum_service")]]
        await msg.reply_text("❌ Avval kanalga obuna bo'ling!\n\n✅ Obuna bo'lgach qayta yuboring.", reply_markup=InlineKeyboardMarkup(kb))
        return
    if msg.document:
        await msg.reply_document(msg.document.file_id, caption="✅ Mana faylingiz!")
    elif msg.photo:
        await msg.reply_photo(msg.photo[-1].file_id, caption="✅ Mana rasmingiz!")
    elif msg.video:
        await msg.reply_video(msg.video.file_id, caption="✅ Mana videongiz!")
    else:
        await msg.reply_text("✅ Qabul qilindi!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
print("Bot ishga tushdi!")
app.run_polling()
