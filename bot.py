import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = os.getenv("BOT_TOKEN")

# قنواتك - لازم تخلي البوت ادمن فيهم عشان يقدر يتأكد
CHANNELS = [
    {"name": "📢 تحديثات البوت", "link": "https://t.me/ricofsj", "username": "@ricofsj"},
    {"name": "🤖 قناة البوت", "link": "https://t.me/hzohzhzj", "username": "@hzohzhzj"},
]

# ======= كل الشروحات جاهزة جوة الكود =======
COURSES = {
    "whatsapp": {
        "title": "💬 شروحات واتساب",
        "lessons": {
            "1": {"t": "1️⃣ تأمين واتساب من الاختراق", "c": "🔐 كيف تأمن واتساب:\n\n1. فعل التحقق بخطوتين: الإعدادات > الحساب > التحقق بخطوتين\n2. لا تدي كود التحقق لاي زول\n3. فعل قفل ببصمة\n4. راجع الأجهزة المرتبطة كل اسبوع: الإعدادات > الأجهزة المرتبطة\n5. اي رابط غريب لا تدوسو\n\n⚠️ البوت للحماية فقط."},
            "2": {"t": "2️⃣ استرجاع حساب واتساب مسروق", "c": "♻️ الاسترجاع:\n\n1. نزل واتساب وسجل برقمك\n2. حيطلب كود 6 ارقام بجي في SMS\n3. اول ما تدخلو، السارق بطلع تلقائيا\n4. فعل التحقق بخطوتين طوالي\n5. لو ما جاك الكود، انتظر 12 ساعة وجرب\n\nرابط دعم واتساب: support.whatsapp.com"},
            "3": {"t": "3️⃣ بوت واتساب ببايثون", "c": "🤖 كيف تعمل بوت واتساب:\n\n```python\nfrom pywhatkit import sendwhatmsg\nimport datetime\n# ارسال رسالة مجدولة\nsendwhatmsg('+249...', 'السلام عليكم', 15, 30)\n```\nالمكتبات: pywhatkit, pyautogui, selenium"},
            "4": {"t": "4️⃣ حماية من روابط الاختراق", "c": "🛡️ الروابط الملغمة:\n\n- اي رابط فيه ip او فيه you won prize = كذب\n- لا تنزل ملفات apk من خارج المتجر\n- فعل Google Play Protect\n- استخدم VirusTotal لفحص الروابط قبل ما تدوس"},
            "5": {"t": "5️⃣ واتساب بيزنس وادواته", "c": "💼 واتساب بيزنس:\n1. فيهو كاتالوج منتجات\n2. ردود تلقائية\n3. رسائل ترحيب\n4. تصنيف العملاء Label\nمفيد للتجار."},
            "6": {"t": "6️⃣ اخفاء الظهور والخصوصية", "c": "👁️‍🗨️ الخصوصية:\nالإعدادات > الخصوصية >\n- اخر ظهور: جهات اتصالي فقط\n- صورة البروفايل: جهات اتصالي\n- قراءة الرسائل: الغي الصحين الزرق\n- المجموعات: جهات اتصالي فقط"},
        }
    },
    "facebook": {
        "title": "📘 شروحات فيسبوك",
        "lessons": {
            "1": {"t": "1️⃣ تأمين فيسبوك 100%", "c": "🔒 التأمين:\n1. فعل المصادقة الثنائية 2FA\n2. كلمة سر قوية 12 حرف\n3. فعل تنبيه تسجيل الدخول\n4. راجع الجلسات النشطة واحذف الغريب\n5. ايميل حقيقي + رقمك"},
            "2": {"t": "2️⃣ استرجاع حساب فيسبوك", "c": "♻️ الاسترجاع:\nادخل facebook.com/hacked\nاكتب ايميلك او رقمك\nاتبع الخطوات وارفع بطاقة هوية لو طلب"},
            "3": {"t": "3️⃣ زيادة متابعين حقيقيين", "c": "📈 النمو:\n1. نزل ريلز يومي\n2. استخدم هاشتاقات\n3. تفاعل مع صفحات كبيرة\n4. اعمل بث مباشر اسبوعي"},
            "4": {"t": "4️⃣ حماية من الصفحات المزورة", "c": "⚠️ الصفحات المزورة بتطلب تسجيل دخولك، دايما تأكد الرابط هو facebook.com فقط، اي رابط تاني زي faceb00k = احتيال"},
            "5": {"t": "5️⃣ انشاء صفحة احترافية", "c": "📄 الصفحة:\n- اسم قصير\n- صورة غلاف واضحة\n- وصف فيه كلمات مفتاحية\n- زر اتصال\n- نشر 3 مرات في الاسبوع"},
            "6": {"t": "6️⃣ الربح من فيسبوك", "c": "💰 الربح:\n- الربح من الريلز\n- الربح من النجوم\n- الربح من الاعلانات في الفيديوهات\nلازم 5000 متابع و 60 الف دقيقة مشاهدة"},
        }
    },
    "instagram": {
        "title": "📸 شروحات انستغرام",
        "lessons": {
            "1": {"t": "1️⃣ تأمين انستغرام", "c": "🔐 الامان:\nفعل 2FA من الإعدادات > الامان > المصادقة الثنائية\nلا تربط حسابك بمواقع زيادة متابعين وهمية"},
            "2": {"t": "2️⃣ استرجاع حساب انستغرام", "c": "♻️ الاسترجاع:\nافتح التطبيق > نسيت كلمة السر > ادخل اليوزر > جرب ايميلك او فيسبوك المرتبط"},
            "3": {"t": "3️⃣ زيادة متابعين", "c": "🚀 النمو:\n1. ريلز 15 ثانية مع ترند\n2. هاشتاق 3 كبير + 3 متوسط + 3 صغير\n3. انشر الساعة 7 مساء"},
            "4": {"t": "4️⃣ تصميم ستوري احترافي", "c": "🎨 استخدم Canva، خطوط عربية، الوان موحدة، لا تكتر كتابة"},
            "5": {"t": "5️⃣ خوارزمية الانستا", "c": "🧠 الخوارزمية بتحب:\n- تفاعل اول 30 دقيقة\n- حفظ البوست\n- مشاركة البوست\n- تعليقات طويلة"},
            "6": {"t": "6️⃣ الربح من انستغرام", "c": "💰 الربح:\n- التسويق بالعمولة\n- بيع منتجاتك\n- الاشتراكات المدفوعة\n- التعاون مع براندات"},
        }
    },
    "tiktok": {
        "title": "🎵 شروحات تيك توك",
        "lessons": {
            "1": {"t": "1️⃣ تأمين تيك توك", "c": "🔐 لا تدخل بمواقع زيادة متابعين، فعل التحقق بخطوتين، اربط ايميل + رقم"},
            "2": {"t": "2️⃣ كيف تطلع اكسبلور", "c": "🔥 اكسبلور:\n1. اول 3 ثواني مهمة\n2. استخدم صوت ترند\n3. هاشتاق #fyp #foryou\n4. انشر 2-3 في اليوم"},
            "3": {"t": "3️⃣ مونتاج فيديو تيك توك", "c": "✂️ استخدم CapCut، قص سريع، زووم، مؤثرات، كلام على الشاشة"},
            "4": {"t": "4️⃣ الربح من تيك توك", "c": "💰 الربح:\n- هدايا اللايف\n- برنامج مكافآت المبدعين\n- التسويق\n- بيع منتجات"},
            "5": {"t": "5️⃣ حل مشكلة 0 مشاهدات", "c": "🚫 0 مشاهدات يعني:\n- محتوى مكرر\n- مخالفة ارشادات\n- حساب جديد، انتظر\n- امسح الفيديو ونزلو بجودة اعلى"},
            "6": {"t": "6️⃣ زيادة متابعين تيك توك", "c": "📈 تابع ترندات، قلدها بطريقتك، تفاعل في التعليقات، اعمل دوتو مع مشاهير"},
        }
    },
    "python": {
        "title": "🐍 شروحات لغة بايثون",
        "lessons": {
            "1": {"t": "1️⃣ تأمين حسابات ببايثون", "c": "🔐 مثال فحص قوة الباسورد:\n```python\nimport re\ndef strong(p):\n  return len(p)>8 and re.search(r'[A-Z]',p)\nprint(strong('MyPass123'))\n```"},
            "2": {"t": "2️⃣ بوت تليجرام ببايثون", "c": "🤖 بوت تليجرام:\n```python\nfrom telegram.ext import Application\n# هذا نفس كود بوتك الحالي\n```\nالمكتبة: python-telegram-bot"},
            "3": {"t": "3️⃣ اساسيات بايثون", "c": "📚 المتغيرات، الحلقات، الشروط، الدوال، القوائم، القواميس. اتعلمها من python.org"},
            "4": {"t": "4️⃣ سكربت فحص الروابط", "c": "🛡️ فحص الروابط:\n```python\nimport requests\ndef check(url):\n  r=requests.get(url)\n  return r.status_code\n```"},
            "5": {"t": "5️⃣ بوت واتساب ببايثون", "c": "💬 مكتبات: selenium, pywhatkit, open-wa. بتحتاج متصفح يشتغل 24 ساعة"},
            "6": {"t": "6️⃣ كيف ترفع بوتك في Render", "c": "☁️ الرفع:\n1. GitHub\n2. Render.com > New Web Service\n3. ضيف BOT_TOKEN\n4. Deploy\nدا انت عملتو هسع!"},
        }
    }
}

async def is_subscribed(bot, user_id):
    not_joined = []
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch["username"], user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(ch)
        except BadRequest:
            # لو البوت ما ادمن، نعتبره ما مشترك عشان نجبر الادمن يخلي البوت ادمن
            not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(c["name"], url=c["link"])] for c in CHANNELS]
    keyboard.append([InlineKeyboardButton("✅ تم الانضمام - تحقق", callback_data="check_join")])
    await update.message.reply_text(
        "👋 مرحب بيك في بوت الشروحات الشامل\n\n🚨 **عليك الانضمام لقنواتنا اولاً عشان يفتح البوت:**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    txt = f"🆔 **معلوماتك:**\n\n👤 الاسم: {u.first_name}\n🆔 الايدي: `{u.id}`\n🔗 اليوزر: @{u.username if u.username else 'مافي'}\n💬 نوع المحادثة: {update.effective_chat.type}"
    await update.message.reply_text(txt, parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = """
📜 **قائمة الاوامر:**

/start - بدء البوت والاشتراك
/id - يجيب ايدي ومعلومات حسابك
/help - عرض هذه القائمة

🔥 **طريقة الاستخدام:**
1. اشترك في القنوات
2. اضغط تحقق
3. اختار القسم (واتساب، فيسبوك...)
4. اختار الدرس

قنواتنا: @ricofsj - @hzohzhzj
"""
    await update.message.reply_text(txt, parse_mode="Markdown")

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "check_join":
        not_joined = await is_subscribed(context.bot, user_id)
        if not_joined:
            kb = [[InlineKeyboardButton(c["name"], url=c["link"])] for c in not_joined]
            kb.append([InlineKeyboardButton("🔄 اعادة التحقق", callback_data="check_join")])
            await query.message.reply_text(
                "❌ **ما انضميت لكل القنوات!**\n\nانضم للقنوات دي واضغط اعادة تحقق 👇",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="Markdown"
            )
            return
        # انضم - اعرض الاقسام
        kb = [[InlineKeyboardButton(v["title"], callback_data=f"cat_{k}")] for k, v in COURSES.items()]
        await query.message.reply_text("✅ تم التحقق! مرحب بيك 🔥\n\nاختار القسم:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("cat_"):
        cat_key = data.split("_")[1]
        course = COURSES[cat_key]
        kb = [[InlineKeyboardButton(v["t"], callback_data=f"les_{cat_key}_{k}")] for k, v in course["lessons"].items()]
        kb.append([InlineKeyboardButton("⬅️ رجوع للاقسام", callback_data="check_join")])
        await query.message.reply_text(f"{course['title']}\n\nاختار الدرس:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("les_"):
        _, cat_key, les_key = data.split("_")
        lesson = COURSES[cat_key]["lessons"][les_key]
        kb = [[InlineKeyboardButton("⬅️ رجوع للدروس", callback_data=f"cat_{cat_key}")]]
        await query.message.reply_text(
            f"{lesson['t']}\n\n{lesson['c']}",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(callbacks))
    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
