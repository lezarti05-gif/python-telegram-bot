import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# === روابط قنواتك الرسمية ===
CHANNELS = {
    "🤖 قناة البوت": "https://t.me/hzohzhzj",
    "📢 تحديثات البوت": "https://t.me/ricofsj"
}

# === الكورسات بتفتح بعد 5 نقاط ===
COURSES = {
    "💻 مجال البرمجة": "https://t.me/hzohzhzj",
    "🎨 مجال التصميم": "https://t.me/ricofsj",
    "💰 شروحات الربح": "https://t.me/hzohzhzj"
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

    # نظام الدعوة
    if args and args[0].startswith("ref_"):
        ref_id = args[0].replace("ref_", "")
        if ref_id != str(user_id):
            ref_user = get_user(data, ref_id)
            if str(user_id) not in ref_user["invited"]:
                ref_user["invited"].append(str(user_id))
                ref_user["points"] += 1
                save_data(data)
                try:
                    await context.bot.send_message(chat_id=int(ref_id), text=f"🎉 مبروك! شخص جديد دخل برابطك، نقاطك الآن {ref_user['points']}/5")
                except:
                    pass

    user = get_user(data, user_id)
    save_data(data)

    bot_username = (await context.bot.get_me()).username
    my_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    text = f"""
أهلا بك يا {update.effective_user.first_name} 👋

🔗 **قنواتنا الرسمية:**
اشترك أولا عشان ما يفوتك شي

⭐ **نقاطك: {user['points']}/5**
ادع 5 اشخاص برابطك عشان تفتح الكورسات
"""

    keyboard = []
    for name, link in CHANNELS.items():
        keyboard.append([InlineKeyboardButton(name, url=link)])
    
    keyboard.append([InlineKeyboardButton(f"⭐ نقاطي: {user['points']}/5", callback_data="points")])
    keyboard.append([InlineKeyboardButton("📤 رابط الدعوة الخاص بي", callback_data="mylink")])

    # عرض الكورسات حسب النقاط
    if user["points"] >= 5:
        text += "\n\n✅ **الكورسات فتحت لك:**"
        for name, link in COURSES.items():
            keyboard.append([InlineKeyboardButton(name, url=link)])
    else:
        need = 5 - user["points"]
        text += f"\n\n🔒 الكورسات مقفلة، باقي لك {need} دع
