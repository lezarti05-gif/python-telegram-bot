import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تفعيل اللوج
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN ما موجود في Render!")

# قنواتك
CHANNELS = [
    {"name": "📢 تحديثات البوت", "link": "https://t.me/ricofsj", "username": "@ricofsj"},
    {"name": "🤖 قناة البوت", "link": "https://t.me/hzohzhzj", "username": "@hzohzhzj"},
]

# الشروحات - 5 اقسام × 6 دروس
COURSES = {
    "whatsapp": {
        "title": "💬 شروحات واتساب",
        "lessons": {
            "1": {"t": "1️⃣ تأمين واتساب من الاختراق", "c": "🔐 كيف تأمن واتساب:\n\n1. الإعدادات > الحساب > التحقق بخطوتين > فعلو\n2. خلي كود من 6 ارقام\n3. فعل قفل ببصمة: الإعدادات > الخصوصية > قفل ببصمة\n4. راجع الأجهزة المرتبطة كل اسبوع\n5. اي رابط غريب لا تدوسو"},
            "2": {"t": "2️⃣ استرجاع واتساب مسروق", "c": "♻️ الاسترجاع:\n\n1. نزل واتساب جديد\n2. دخل رقمك\n3. بجيك كود SMS دخلو\n4. السارق بطلع تلقائيا\n5. فعل التحقق بخطوتين فورا"},
            "3": {"t": "3️⃣ بوت واتساب ببايثون", "c": "🤖 بوت واتساب:\n```python\nfrom pywhatkit import sendwhatmsg\nsendwhatmsg('+249xxxx','مرحبا',15,30)\n```\nالمكتبات: pywhatkit, selenium"},
            "4": {"t": "4️⃣ حماية من روابط الاختراق", "c": "🛡️ الروابط الملغمة:\n- لا تدوس رابط فيه جائزة\n- افحص الرابط في موقع virustotal.com\n- لا تنزل ملفات apk خارج المتجر"},
            "5": {"t": "5️⃣ واتساب بيزنس", "c": "💼 واتساب بيزنس:\n1. كاتالوج منتجات\n2. ردود تلقائية\n3. رسائل ترحيب\n4. تصنيف العملاء"},
            "6": {"t": "6️⃣ اخفاء الظهور", "c": "👁️ الخصوصية:\nالإعدادات > الخصوصية > اخر ظهور > جهات اتصالي فقط\nصورة البروفايل > جهات اتصالي\nالقراءة > الغي الصحين الزرق"},
        }
    },
    "facebook": {
        "title": "📘 شروحات فيسبوك",
        "lessons": {
            "1": {"t": "1️⃣ تأمين فيسبوك 100%", "c": "🔒 التأمين:\n1. فعل المصادقة الثنائية 2FA\n2. كلمة سر 12 حرف\n3. تنبيه تسجيل الدخول\n4. احذف الجلسات الغريبة"},
            "2": {"t": "2️⃣ استرجاع فيسبوك", "c": "♻️ ادخل: facebook.com/hacked\nاكتب ايميلك واتبع الخطوات"},
            "3": {"t": "3️⃣ زيادة متابعين", "c": "📈 نزل ريلز يومي + هاشتاقات + بث مباشر"},
            "4": {"t": "4️⃣ حماية من الصفحات المزورة", "c": "⚠️ تأكد الرابط هو facebook.com فقط، اي رابط تاني احتيال"},
            "5": {"t": "5️⃣ انشاء صفحة احترافية", "c": "📄 اسم قصير + غلاف واضح + نشر 3 مرات في الاسبوع"},
            "6": {"t": "6️⃣ الربح من فيسبوك", "c": "💰 5000 متابع + 60 الف دقيقة مشاهدة = تفعل الربح"},
        }
    },
    "instagram": {
        "title": "📸 شروحات انستغرام",
        "lessons": {
            "1": {"t": "1️⃣ تأمين انستغرام", "c": "🔐 فعل 2FA من الإعدادات > الامان"},
            "2": {"t": "2️⃣ استرجاع انستغرام", "c": "♻️ نسيت كلمة السر > دخل اليوزر > استرجع بالايميل"},
            "3": {"t": "3️⃣ زيادة متابعين", "c": "🚀 ريلز 15 ثانية + ترند + انشر 7 مساء"},
            "4": {"t": "4️⃣ تصميم ستوري", "c": "🎨 استخدم Canva، الوان موحدة"},
            "5": {"t": "5️⃣ خوارزمية الانستا", "c": "🧠 بتحب: حفظ البوست + مشاركة + تعليقات طويلة"},
            "6": {"t": "6️⃣ الربح من انستغرام", "c": "💰 تسويق بالعمولة + بيع منتجات"},
        }
    },
    "tiktok": {
        "title": "🎵 شروحات تيك توك",
        "lessons": {
            "1": {"t": "1️⃣ تأمين تيك توك", "c": "🔐 فعل تحقق بخطوتين + اربط ايميل"},
            "2": {"t": "2️⃣ كيف تطلع اكسبلور", "c": "🔥 اول 3 ثواني مهمة + صوت ترند + #fyp"},
            "3": {"t": "3️⃣ مونتاج تيك توك", "c": "✂️ استخدم CapCut، قص سريع + زووم"},
            "4": {"t": "4️⃣ الربح من تيك توك", "c": "💰 هدايا اللايف + مكافآت المبدعين"},
            "5": {"t": "5️⃣ حل 0 مشاهدات", "c": "🚫 محتوى مكرر او مخالفة، امسح ونزل بجودة اعلى"},
            "6": {"t": "6️⃣ زيادة متابعين", "c": "📈 قلد الترندات + دوتو مع مشاهير"},
        }
    },
    "python": {
        "title": "🐍 شروحات بايثون",
        "lessons": {
            "1": {"t": "1️⃣ فحص قوة الباسورد", "c": "🔐 كود:\n```python\nimport re\ndef strong(p):\n return len(p)>8\n```"},
            "2": {"t": "2️⃣ بوت تليجرام", "c": "🤖 نفس كود بوتك دا هو بوت تليجرام!"},
            "3": {"t": "3️⃣ اساسيات بايثون", "c": "📚 متغيرات، حلقات، شروط، دوال"},
            "4": {"t": "4️⃣ فحص الروابط", "c": "🛡️ كود فحص:\n```python\nimport requests\nprint(requests.get(url).status_code)\n```"},
            "5": {"t": "5️⃣ بوت واتساب", "c": "💬 مكتبات: selenium, pywhatkit"},
            "6": {"t": "6️⃣ رفع البوت في Render", "c": "☁️ GitHub > Render > ضيف BOT_TOKEN > Deploy"},
        }
    }
}

async def check_sub(bot, user_id):
    not_joined = []
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(chat_id=ch["username"], user_id=user_id)
            if m.status in ['left', 'kicked']:
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton(c["name"], url=c["link"])] for c in CHANNELS]
    kb.append([InlineKeyboardButton("✅ تم الانضمام - تحقق", callback_data="check")])
    await update.message.reply_text(
        "👋 اهلا بيك في بوت الشروحات\n\n🚨 لازم تنضم لقنواتنا اول:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🆔 معلوماتك:\n\n👤 الاسم: {u.first_name}\n🆔 الايدي: `{u.id}`\n🔗 اليوزر: @{u.username if u.username else 'لا يوجد'}",
        parse_mode="Markdown"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 الاوامر:\n\n/start - بدء البوت\n/id - يجيب ايدي ومعلوماتك\n/help - قائمة الاوامر\n\nاشترك في القنوات واضغط تحقق عشان تفتح الشروحات."
    )

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "check":
        not_joined = await check_sub(context.bot, user_id)
        if not_joined:
            kb = [[InlineKeyboardButton(c["name"], url=c["link"])] for c in not_joined]
            kb.append([InlineKeyboardButton("🔄 اعادة التحقق", callback_data="check")])
            await query.message.reply_text("❌ لسه ما انضميت لكل القنوات! انضم واضغط اعادة تحقق:", reply_markup=InlineKeyboardMarkup(kb))
            return
        kb = [[InlineKeyboardButton(v["title"], callback_data=f"cat_{k}")] for k, v in COURSES.items()]
        await query.message.reply_text("✅ تم التحقق بنجاح! اختار القسم:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("cat_"):
        cat = data.split("_")[1]
        course = COURSES[cat]
        kb = [[InlineKeyboardButton(v["t"], callback_data=f"les_{cat}_{k}")] for k, v in course["lessons"].items()]
        kb.append([InlineKeyboardButton("⬅️ رجوع", callback_data="check")])
        await query.message.reply_text(f"{course['title']}:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("les_"):
        _, cat, les = data.split("_")
        lesson = COURSES[cat]["lessons"][les]
        kb = [[InlineKeyboardButton("⬅️ رجوع للدروس", callback_data=f"cat_{cat}")]]
        await query.message.reply_text(f"{lesson['t']}\n\n{lesson['c']}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler(["Id","ID"], id_cmd))
    app.add_handler(CommandHandler(["Help","HELP"], help_cmd))
    app.add_handler(CallbackQueryHandler(on_callback))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
