import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# === هنا خت روابط قنواتك الحقيقية ===
CHANNELS = {
    "قناة الشروحات 📚": "https://t.me/your_channel1",
    "قناة المجالات 💼": "https://t.me/your_channel2",
    "قناة التحديثات 📢": "https://t.me/your_channel3"
}

# === دي الكورسات البتفتح بعد 5 نقاط ===
COURSES = {
    "مجال البرمجة": "https://t.me/your_channel1/10",
    "مجال التصميم": "https://t.me/your_channel2/10",
    "شروحات الربح": "https://t.me/your_channel3/10"
}

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user(data, user_id):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"points": 0, "invited": []}
    return data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id = update.effective_user.id
    args = context.args

    # نظام الاحالة - لو زول جا برابط زول
    if args and args[0].startswith("ref_"):
        ref_id = args[0].replace("ref_", "")
        if ref_id != str(user_id):
            ref_user = get_user(data, ref_id)
            if str(user_id) not in ref_user["invited"]:
                ref_user["invited"].append(str(user_id))
                ref_user["points"] += 1
                save_data(data)

    user = get_user(data, user_id)
    save_data(data)

    bot_username = (await context.bot.get_me()).username
    my_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    keyboard = []
    for name, link in CHANNELS.items():
        keyboard.append([InlineKeyboardButton(name, url=link)])
    
    keyboard.append([InlineKeyboardButton(f"نقاطي: {user['points']}/5 ✅", callback_data="points")])
    keyboard.append([InlineKeyboardButton("📤 مشاركة رابطي", url=f"https://t.me/share/url?url={my_link}&text=تعال اربح كورسات مجانية من البوت")])
    
    if user["points"] >= 5:
        keyboard.append([InlineKeyboardButton("🎓 فتح الكورسات", callback_data="courses")])
    else:
        keyboard.append([InlineKeyboardButton(f"🔒 الكورسات مقفلة - باقي {5 - user['points']}", callback_data="locked")])

    text = f"""
👋 مرحبا بيك!

📌 **الخطوة 1: اشترك في قنواتنا**

✅ **الخطوة 2: بعد الاشتراك ده رابطك الخاص:**
`{my_link}`

👥 كل زول يدخل من رابطك تاخد نقطة
🎯 تجيب 5 نقاط بيتفتح ليك كل الكورسات

📊 نقاطك الحالية: {user['points']}/5
"""

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_data()
    user_id = query.from_user.id
    user = get_user(data, user_id)

    if query.data == "points":
        await query.answer(f"نقاطك: {user['points']}/5", show_alert=True)
    elif query.data == "locked":
        await query.answer(f"لازم تجيب 5 اشخاص، باقي ليك {5 - user['points']}", show_alert=True)
    elif query.data == "courses":
        if user["points"] >= 5:
            kb = []
            for name, link in COURSES.items():
                kb.append([InlineKeyboardButton(name, url=link)])
            await query.message.reply_text("🎉 مبروك فتحت الكورسات:\n", reply_markup=InlineKeyboardMarkup(kb))
        else:
            await query.answer(f"لسه ما كملت، باقي ليك {5 - user['points']}", show_alert=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
