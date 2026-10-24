import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

GROUPS = [
    ("قروبنا الاساسي 🔐", "https://t.me/yourgroup1"),
    ("قناة الشروحات 📢", "https://t.me/yourgroup2"),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, url=link)] for name, link in GROUPS]
    keyboard.append([InlineKeyboardButton("✅ تم الانضمام - شوف العروض", callback_data="joined")])
    await update.message.reply_text(
        "👋 مرحبا!\n\n🚨 لازم تنضم للقروبات دي اول عشان تشوف عروض الهكر لله:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "joined":
        text = "🔥 عروض تعليم الحماية والهكر الاخلاقي\n\n1️⃣ حماية الحسابات\n2️⃣ كورس مجاني\n\nلله والتعليم فقط"
        kb = [[InlineKeyboardButton("1️⃣ الحماية", callback_data="c1")]]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
