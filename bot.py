import os, threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SITE = "https://kgk.mycollege.kz/"

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

user_lang = {}
waiting_question = set()

TEXT = {
    "ru": {
        "welcome": "🏫✨ КАРАГАНДИНСКИЙ ВЫСШИЙ ГУМАНИТАРНЫЙ КОЛЛЕДЖ ✨🏫\n\n👋 Привет! Я бот КГК\n\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40\n🏠 Общежитие: есть, бесплатно\n🎓 С 1976 года готовим учителей и воспитателей\n\nВыбери кнопку ниже 👇",
        "schedule": "📅 РАСПИСАНИЕ\n\nАктуальное расписание — на сайте колледжа 👇\n",
        "specs": "📚 СПЕЦИАЛЬНОСТИ КГК:\n\n🧒 01120100 — Дошкольное воспитание и обучение\nКвалификация: Воспитатель детского сада\n\n📖 01110100 — Педагогика и методика начального обучения\nКвалификация: Учитель начальных классов\n\n🎨 01130200 — Дополнительное образование\nКвалификация: Педагог доп. образования\n\n🎵 Музыка\n🏃 Физкультура",
        "admission": "🎓 ПОСТУПЛЕНИЕ\n\n📌 Документы:\n• Аттестат (9 / 11 кл.)\n• Удостоверение личности\n• Фото 3x4 — 4 шт\n• Мед. справка 075-У\n\n📅 Прием: 25 июня — 25 августа\n🎓 Есть ГРАНТ — бесплатно!\n🏠 Общежитие: есть, бесплатно\n📞 +7 (7212) 41-16-92",
        "pay": "💰 ГРАНТЫ / ОПЛАТА\n\n🎓 Грант: бесплатно + стипендия\n💳 Платно: 250 000 тг\n🏠 Общежитие: бесплатно\n📞 +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40",
        "contacts": "📞 КОНТАКТЫ КГК\n\n🏫 Карагандинский высший гуманитарный колледж\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 г. Караганда, пр. Нурсултана Назарбаева, 22\n📞 Приемная: +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40\n🕐 Пн-Пт 09:00 — 18:00\n🚫 Сб-Вс — выходной\n🏠 Общежитие: есть, бесплатно\n\n📱 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg",
        "news": "📰 НОВОСТИ\n\n🎓 Открыт набор на 2026-2027 учебный год\n🏫 В 2026 году колледжу — 50 ЛЕТ!\n👩‍🏫 Наши выпускники работают в школах и садах Караганды",
        "site": "🌐 Официальный сайт КГК:\n",
        "social": "📱 СОЦСЕТИ КГК\n\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg\n\nПодписывайся, там вся жизнь колледжа! ❤️",
        "ask": "❓ Напиши свой вопрос одним сообщением!",
        "ask_sent": "✅ Спасибо! Твой вопрос принят.\n\n📞 Если срочно — позвони нам:\n+7 (7212) 41-16-92\n📍 пр. Назарбаева, 22",
        "ask_btn": "❓ Задать вопрос",
        "lang_btn": "🌐 Язык / Тіл",
        "social_btn": "📱 Соцсети",
    },
    "kz": {
        "welcome": "🏫✨ ҚАРАҒАНДЫ ЖОҒАРЫ ГУМАНИТАРЛЫҚ КОЛЛЕДЖІ ✨🏫\n\n👋 Сәлем! Мен ҚГК ботымын\n\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40\n🏠 Жатақхана: бар, тегін\n🎓 1976 жылдан бастап мұғалімдер мен тәрбиешілерді даярлаймыз\n\nТөменнен батырманы таңда 👇",
        "schedule": "📅 САБАҚ КЕСТЕСІ\n\nӨзекті кесте — колледж сайтында 👇\n",
        "specs": "📚 ҚГК МАМАНДЫҚТАРЫ:\n\n🧒 01120100 — Мектепке дейінгі тәрбие және оқыту\nБіліктілігі: Балабақша тәрбиешісі\n\n📖 01110100 — Бастауыш оқытудың педагогикасы мен әдістемесі\nБіліктілігі: Бастауыш сынып мұғалімі\n\n🎨 01130200 — Қосымша білім беру\nБіліктілігі: Қосымша білім беру педагогы\n\n🎵 Музыка\n🏃 Дене шынықтыру",
        "admission": "🎓 ОҚУҒА ТҮСУ\n\n📌 Құжаттар:\n• Аттестат (9 / 11 сынып)\n• Жеке куәлік\n• Фото 3x4 — 4 дана\n• Мед. анықтама 075-У\n\n📅 Қабылдау: 25 маусым — 25 тамыз\n🎓 ГРАНТ бар — тегін!\n🏠 Жатақхана: бар, тегін\n📞 +7 (7212) 41-16-92",
        "pay": "💰 ГРАНТ / ТӨЛЕМ\n\n🎓 Грант: тегін + шәкіртақы\n💳 Ақылы: 250 000 тг\n🏠 Жатақхана: тегін\n📞 +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40",
        "contacts": "📞 БАЙЛАНЫС ҚГК\n\n🏫 Қарағанды жоғары гуманитарлық колледжі\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 Қарағанды қ., Нұрсұлтан Назарбаев даңғылы, 22\n📞 Қабылдау комиссиясы: +7 (7212) 41-16-92\n📞 56-12-70, 56-05-40\n🕐 Дс-Жм 09:00 — 18:00\n🚫 Сб-Жс — демалыс\n🏠 Жатақхана: бар, тегін\n\n📱 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg",
        "news": "📰 ЖАҢАЛЫҚТАР\n\n🎓 2026-2027 оқу жылына қабылдау ашық\n🏫 2026 жылы колледжге — 50 ЖЫЛ!\n👩‍🏫 Біздің түлектер Қарағандының мектептері мен балабақшаларында жұмыс істейді",
        "site": "🌐 ҚГК ресми сайты:\n",
        "social": "📱 ҚГК ӘЛЕУМЕТТІК ЖЕЛІЛЕРІ\n\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg\n\nЖазыл, колледж өмірі сонда! ❤️",
        "ask": "❓ Сұрағыңды бір хабарламамен жаз!",
        "ask_sent": "✅ Рахмет! Сұрағың қабылданды.\n\n📞 Шұғыл болса — хабарлас:\n+7 (7212) 41-16-92\n📍 Назарбаев даңғылы, 22",
        "ask_btn": "❓ Сұрақ қою",
        "lang_btn": "🌐 Тіл / Язык",
        "social_btn": "📱 Әлеуметтік желілер",
    }
}

def lang_of(uid):
    return user_lang.get(uid, "ru")

def main_menu(lang):
    t = TEXT[lang]
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "ru":
        m.add(
            types.KeyboardButton("📅 Расписание"), types.KeyboardButton("📚 Специальности"),
            types.KeyboardButton("🎓 Поступление"), types.KeyboardButton("💰 Гранты / Оплата"),
            types.KeyboardButton("📞 Контакты"), types.KeyboardButton("📰 Новости"),
            types.KeyboardButton("🌐 Сайт колледжа"), types.KeyboardButton(t["social_btn"]),
            types.KeyboardButton(t["ask_btn"]), types.KeyboardButton(t["lang_btn"]),
        )
    else:
        m.add(
            types.KeyboardButton("📅 Сабақ кестесі"), types.KeyboardButton("📚 Мамандықтар"),
            types.KeyboardButton("🎓 Оқуға түсу"), types.KeyboardButton("💰 Грант / Төлем"),
            types.KeyboardButton("📞 Байланыс"), types.KeyboardButton("📰 Жаңалықтар"),
            types.KeyboardButton("🌐 Колледж сайты"), types.KeyboardButton(t["social_btn"]),
            types.KeyboardButton(t["ask_btn"]), types.KeyboardButton(t["lang_btn"]),
        )
    return m

def site_btn(lang):
    m = types.InlineKeyboardMarkup()
    txt = "🌐 Открыть сайт" if lang == "ru" else "🌐 Сайтты ашу"
    m.add(types.InlineKeyboardButton(txt, url=SITE))
    return m

def social_btn(lang):
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/gumanitaricollegeinkrg"))
    m.add(types.InlineKeyboardButton("🎵 TikTok", url="https://tiktok.com/@gumlife_krg"))
    m.add(types.InlineKeyboardButton("🌐 Сайт", url=SITE))
    return m

def lang_keyboard():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇰🇿 Қазақша"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=lang_keyboard())

@bot.message_handler(func=lambda m: m.text in ["🇷🇺 Русский", "🇰🇿 Қазақша", "🌐 Язык / Тіл", "🌐 Тіл / Язык"])
def set_lang(message):
    if message.text == "🇷🇺 Русский":
        user_lang[message.chat.id] = "ru"
    elif message.text == "🇰🇿 Қазақша":
        user_lang[message.chat.id] = "kz"
    else:
        bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=lang_keyboard())
        return
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["welcome"], reply_markup=main_menu(lang))

@bot.message_handler(func=lambda m: m.text in ["📅 Расписание", "📅 Сабақ кестесі"])
def schedule(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["schedule"] + SITE, reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["📚 Специальности", "📚 Мамандықтар"])
def specs(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["specs"], reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["🎓 Поступление", "🎓 Оқуға түсу"])
def admission(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["admission"], reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["💰 Гранты / Оплата", "💰 Грант / Төлем"])
def pay(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["pay"], reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["📞 Контакты", "📞 Байланыс"])
def contacts(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["contacts"], reply_markup=social_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["📰 Новости", "📰 Жаңалықтар"])
def news(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["news"], reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["🌐 Сайт колледжа", "🌐 Колледж сайты"])
def site(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["site"] + SITE, reply_markup=site_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["📱 Соцсети", "📱 Әлеуметтік желілер"])
def social(message):
    lang = lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["social"], reply_markup=social_btn(lang))

@bot.message_handler(func=lambda m: m.text in ["❓ Задать вопрос", "❓ Сұрақ қою"])
def ask_start(message):
    lang = lang_of(message.chat.id)
    waiting_question.add(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["ask"])

@bot.message_handler(func=lambda m: True)
def other(message):
    lang = lang_of(message.chat.id)
    if message.chat.id in waiting_question:
        waiting_question.remove(message.chat.id)
        print(f"ВОПРОС от {message.from_user.username}: {message.text}")
        bot.send_message(message.chat.id, TEXT[lang]["ask_sent"], reply_markup=main_menu(lang))
    else:
        bot.send_message(message.chat.id, TEXT[lang]["welcome"], reply_markup=main_menu(lang))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()
