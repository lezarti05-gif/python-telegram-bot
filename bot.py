import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# ====== روابطك الحقيقية ======
GROUPS = [
    ("📢 تحديثات البوت", "https://t.me/ricofsj"),
    ("🤖 قناة البوت", "https://t.me/hzohzhzj"),
]

COURSES = {
    "تصميم": {
        "اسم": "🎨 مجال التصميم",
        "دروس": {
            "11": "الدرس الأول: تطبيقات اريد تصميم للمبتدئين",
            "12": "الدرس الثاني: كيف تصمم شعار ب 5 دقايق وتبيعو",
            "13": "الدرس الثالث: اساسيات التصميم الاحترافي",
            "14": "الدرس الرابع: الربح من التصميم 💰"
        }
    },
    "الربح": {
        "اسم": "💰 شروحات الربح العام",
        "دروس": {
            "11": "الدرس الأول: الربح من الاختصار",
            "12": "الدرس الثاني: الربح من قنوات التيليجرام",
            "13": "الدرس الثالث: الربح من المشاهدات",
            "14": "الدرس الرابع: كيف تجيب اول $100"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for name, link in GROUPS:
        keyboard.append([InlineKeyboardButton(name, url=link)])
    keyboard.append([InlineKeyboardButton("✅ تم الانضمام - دخول البوت", callback_data="joined")])
    
    text = """
أهلا بيك يا بطل! 👋

🚨 **عليك الانضمام للمجموعات التالية قبل استخدام البوت:**

انضم للقناتين تحت واضغط تم الانضمام 👇
"""
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "joined":
        keyboard = []
        for key, course in COURSES.items():
            keyboard.append([InlineKeyboardButton(course["اسم"], callback_data=f"cat_{key}")])
        await query.message.reply_text("🔥 اختار المجال:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("cat_"):
        cat_key = data.replace("cat_", "")
        course = COURSES.get(cat_key)
        if not course:
            return
        keyboard = []
        for lesson_id, lesson_title in course["دروس"].items():
            keyboard.append([InlineKeyboardButton(lesson_title, callback_data=f"lesson_{cat_key}_{lesson_id}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="joined")])
        await query.message.reply_text(f"📚 {course['اسم']}\n\nاختر الدرس:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("lesson_"):
        parts = data.split("_")
        cat_key = parts[1]
        title = COURSES[cat_key]["دروس"][parts[2]]
        await query.message.reply_text(
            f"📖 {title}\n\nالشرح الكامل نزل في قناة البوت 👇\nhttps://t.me/hzohzhzj",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع للاقسام", callback_data="joined")]])
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
