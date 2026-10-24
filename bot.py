import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHANNEL_1 = "@hzohzhzj"
CHANNEL_1_LINK = "https://t.me/hzohzhzj"
CHANNEL_2 = "@ricofsj"
CHANNEL_2_LINK = "https://t.me/ricofsj"

# سيرفر وهمي عشان Render ما يعمل Timed Out
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

TUTORIALS = {
    "whatsapp": {
        "title": "📱 شروحات واتساب",
        "subs": {
            "تأمين حساب واتساب": "🔐 **تأمين واتساب:**\n1. الاعدادات > الحساب > التحقق بخطوتين\n2. ضع PIN من 6 ارقام\n3. اضف بريد استرجاع\n4. لا تشارك كود التحقق مع اي شخص ابدا\n5. فعل قفل البصمة.",
            "استرجاع رسائل محذوفة": "♻️ **استرجاع الرسائل:**\n1. تأكد عندك نسخ في Google Drive\n2. احذف الواتساب وثبته تاني\n3. اضغط استرجاع عند التثبيت\n4. للايفون من iCloud.",
            "القفل بالبصمة": "🔒 **القفل:**\nالاعدادات > الخصوصية > قفل التطبيق > فعل البصمة.\nكدا محدش يفتح واتسابك.",
            "اخفاء الظهور والصحين": "👁️ **الخصوصية:**\nالاعدادات > الخصوصية:\n- اخر ظهور: لا احد\n- الصحين الزرق: الغاء\n- الصورة والحالة: جهاتي فقط.",
            "واتساب اعمال": "💼 **واتساب بزنس:**\n1. نزل WhatsApp Business\n2. انشئ ملف تجاري\n3. استخدم الردود السريعة\n4. اعمل كتالوج منتجات.",
            "نقل واتساب لتلفون جديد": "📲 **النقل:**\nاندرويد لاندرويد: نسخ قوقل درايف\nاندرويد لايفون: Move to iOS\nايفون لاندرويد: Smart Switch."
        }
    },
    "facebook": {
        "title": "📘 شروحات فيسبوك",
        "subs": {
            "تأمين حساب فيسبوك": "🔐 **تأمين 100%:**\n1. الاعدادات > الامان > المصادقة الثنائية\n2. فعل عبر تطبيق مصادقة\n3. فعل تنبيهات الدخول\n4. احذف الجلسات الغريبة.",
            "استرجاع حساب معطل": "🔓 **الاسترجاع:**\n1. facebook.com/hacked\n2. اختر تم اختراقي\n3. ارفع هويتك\n4. انتظر 24 ساعة.",
            "زيادة المتابعين": "📈 **زيادة التفاعل:**\n- 3 منشورات يوميا\n- استخدم ريلز قصير\n- تفاعل اول 30 دقيقة\n- 3 هاشتاق فقط.",
            "توثيق الصفحة": "✅ **التوثيق:**\n10k متابع + محتوى اصلي + طلب Meta Verified + هوية واضحة.",
            "الربح من فيسبوك": "💰 **الربح:**\n5000 متابع + 60 الف دقيقة مشاهدة + قدم من Creator Studio + اربط بنك.",
            "اخفاء الاصدقاء": "🙈 **الخصوصية:**\nالاعدادات > الخصوصية > من يرى اصدقائك: انا فقط."
        }
    },
    "instagram": {
        "title": "📸 شروحات انستغرام",
        "subs": {
            "تأمين حساب انستا": "🔐 **التأمين:**\nالاعدادات > الامان > المصادقة الثنائية > فعل عبر WhatsApp + احفظ رموز الاسترداد.",
            "استرجاع مسروق": "🚨 **استرجاع:**\nنسيت كلمة السر؟ > لا استطيع الوصول؟ > دعم + فيديو سيلفي.",
            "زيادة متابعين": "🚀 **النمو:**\n- ريلز يومي 7 ثواني\n- صوت ترند\n- هاشتاق 5 صغير + 2 كبير\n- نشر 8 صباحا و 8 مساء.",
            "توثيق الحساب": "💙 **التوثيق:**\nالاعدادات > الحساب > طلب التحقق + هوية + شهرة.",
            "حل الحظر": "⛔ **فك الحظر:**\nلا تعمل فولو سريع + لا تكرر تعليق + انتظر 72 ساعة + احذف تطبيقات طرف ثالث.",
            "حساب احترافي": "📊 **احترافي:**\nالاعدادات > الحساب > التبديل لاحترافي = احصائيات واعلانات."
        }
    },
    "tiktok": {
        "title": "🎵 شروحات تيك توك",
        "subs": {
            "تأمين حساب تيك توك": "🔐 **التأمين:**\nالاعدادات > الامان > تحقق بخطوتين SMS + بريد + باسورد قوي.",
            "شروط الربح": "💸 **الربح:**\n10k متابع + 100k مشاهدة 30 يوم + عمر 18+ + قدم من Creativity Program.",
            "كيف تصبح ترند": "🔥 **ترند:**\nاول 3 ثواني مهمة + صوت ترند بدري + 2 فيديو يوميا + مدة 21-34 ثانية.",
            "حل 0 مشاهدة": "👁️ **حل 0 view:**\nاحذف المخالف + لا تنشر معاد + لا تضع رابط اول اسبوع + تفاعل 20 دقيقة قبل النشر.",
            "زيادة المتابعين": "📈 **متابعين:**\nتحدي + دويتو + تعليق يجيب لايكات + بث مباشر يومي.",
            "تحميل بدون علامة": "⬇️ **بدون علامة:**\nاستخدم SnapTik او بوت @TTSaveBot"
        }
    },
    "python": {
        "title": "🐍 شروحات بايثون",
        "subs": {
            "تثبيت بايثون": "💻 **التثبيت:**\npython.org > نزل 3.12 > علم على Add to PATH > تأكد بـ python --version",
            "متغيرات": "📦 **المتغيرات:**\n```python\nname = \"Ahmed\"\nage = 20\nprint(name)\n```",
            "شروط if": "🔀 **if:**\n```python\nif age >= 18:\n    print(\"بالغ\")\nelse:\n    print(\"قاصر\")\n```",
            "حلقات Loops": "🔁 **Loops:**\n```python\nfor i in range(5):\n    print(i)\n```",
            "بوت تيليجرام": "🤖 **البوت:**\n@BotFather > /newbot > احفظ التوكن > استخدم python-telegram-bot",
            "الاستضافة": "☁️ **مجاني:**\nGitHub > Render.com > Web Service > ضع BOT_TOKEN > python bot.py"
        }
    }
}

async def check_joined(user_id, context):
    try:
        m1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        m2 = await context.bot.get_chat_member(CHANNEL_2, user_id)
        return m1.status in ['member','administrator','creator'] and m2.status in ['member','administrator','creator']
    except:
        return False

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 قناة البوت", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton("📢 تحديثات البوت", url=CHANNEL_2_LINK)],
        [InlineKeyboardButton("✅ تم الانضمام", callback_data="check_join")]
    ])

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 واتساب", callback_data="cat_whatsapp"), InlineKeyboardButton("📘 فيسبوك", callback_data="cat_facebook")],
        [InlineKeyboardButton("📸 انستغرام", callback_data="cat_instagram"), InlineKeyboardButton("🎵 تيك توك", callback_data="cat_tiktok")],
        [InlineKeyboardButton("🐍 بايثون", callback_data="cat_python")],
        [InlineKeyboardButton("🆔 ايدي", callback_data="my_id"), InlineKeyboardButton("❓ مساعدة", callback_data="my_help")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_joined(user_id, context):
        await update.message.reply_text(f"مرحبا {update.effective_user.first_name} 👋\nاختر القسم:", reply_markup=main_menu_keyboard())
    else:
        await update.message.reply_text("⚠️ **يجب الاشتراك اولا**\n\nاشترك في القناتين ديل وبعدها اضغط تم الانضمام:", reply_markup=join_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "check_join":
        if await check_joined(user_id, context):
            await query.edit_message_text(f"تم ✅ اهلا {query.from_user.first_name}\nاختر القسم:", reply_markup=main_menu_keyboard())
        else:
            await query.answer("❌ لسه ما اشتركت! لازم تشترك في القناتين.", show_alert=True)
    elif data.startswith("cat_"):
        cat_key = data.replace("cat_", "")
        cat = TUTORIALS[cat_key]
        buttons = []
        for idx, title in enumerate(cat["subs"].keys()):
            buttons.append([InlineKeyboardButton(title, callback_data=f"sub_{cat_key}_{idx}")])
        buttons.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")])
        await query.edit_message_text(f"{cat['title']}\n\nاختر شرح:", reply_markup=InlineKeyboardMarkup(buttons))
    elif data.startswith("sub_"):
        _, cat_key, idx = data.split("_")
        idx = int(idx)
        cat = TUTORIALS[cat_key]
        sub_title = list(cat["subs"].keys())[idx]
        sub_content = list(cat["subs"].values())[idx]
        buttons = [[InlineKeyboardButton("⬅️ رجوع", callback_data=f"cat_{cat_key}")],[InlineKeyboardButton("🏠 رئيسية", callback_data="back_main")]]
        await query.edit_message_text(f"**{sub_title}**\n\n{sub_content}", reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")
    elif data == "back_main":
        await query.edit_message_text("اختر القسم:", reply_markup=main_menu_keyboard())
    elif data == "my_id":
        u = query.from_user
        text = f"🆔 **معلوماتك:**\n\n👤 الاسم: {u.first_name}\n🆔 الايدي: `{u.id}`\n🔗 يوزر: @{u.username if u.username else 'لا يوجد'}"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]]), parse_mode="Markdown")
    elif data == "my_help":
        help_text = "❓ **الاوامر:**\n\n/start - بدء البوت\nid - معرفة ايديك\nhelp - المساعدة"
        await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]]), parse_mode="Markdown")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if text == "id":
        u = update.effective_user
        await update.message.reply_text(f"🆔 ايديك: `{u.id}`\nاسمك: {u.first_name}\nيوزرك: @{u.username if u.username else 'لا يوجد'}", parse_mode="Markdown")
    elif text in ["help","هيلب","مساعدة","الاوامر"]:
        await update.message.reply_text("❓ **الاوامر:**\n/start - رئيسية\nid - ايديك\nhelp - مساعدة", parse_mode="Markdown")
    else:
        await start(update, context)

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
