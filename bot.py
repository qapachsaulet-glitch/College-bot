import os, threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SITE = "https://kgk.mycollege.kz/"
ADMIN_ID = 123456789  # <-- ТВОЙ ID, не забудь
PHOTO_URL = "https://i.postimg.cc/XXXXXXXX/photo.jpg"

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

user_lang = {}
waiting_question = set()
quiz_state = {} # {chat_id: [q_index, scores]}

TEXT = {
  "ru": {
    "welcome": "👋 Привет! Я бот Карагандинского высшего гуманитарного колледжа — КГК\n\n🏫 С 1976 года готовим учителей и воспитателей\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 +7 (7212) 41-16-92\n\nВыбери кнопку ниже 👇",
    "specs": "📚 СПЕЦИАЛЬНОСТИ КГК:\n\n🧒 01120100 — Дошкольное воспитание\n📖 01110100 — Педагогика начального обучения\n🎨 01130200 — Доп. образование",
    "admission": "🎓 ПОСТУПЛЕНИЕ\n\n📌 Документы:\n• Аттестат (9/11 кл.)\n• Удостоверение личности\n• Фото 3x4 — 4 шт\n• Мед. справка 075-У\n\n📅 Прием: 25 июня — 25 августа\n🎓 Есть ГРАНТ!",
    "pay": "💰 ГРАНТЫ / ОПЛАТА\n\n🎓 Грант: бесплатно + стипендия\n💳 Платно: уточняй в приемной\n📞 +7 (7212) 41-16-92",
    "contacts": "📞 КОНТАКТЫ КГК\n\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 +7 (7212) 41-16-92\n🕐 Пн-Пт 09:00 — 18:00",
    "news": "📰 НОВОСТИ\n\n🎓 Открыт набор на 2026-2027 учебный год\n🏫 В 2026 году колледжу — 50 ЛЕТ!",
    "teachers": "👩‍🏫 НАШИ ПРЕПОДАВАТЕЛИ\n\n👩‍🏫 Ахметова А.К. — Педагогика, 20 лет опыта\n👨‍🏫 Сериков Б.М. — Методика начального обучения\n👩‍🎨 Омарова Д.С. — Музыка и творчество\n👩‍🏫 Калиева Н.Т. — Психология и дошкольное воспитание\n\nВсе преподаватели — с высшим образованием и большим опытом!",
    "reviews": "💬 ОТЗЫВЫ ВЫПУСКНИКОВ\n\n⭐ Аяулым, 2023: «Поступила сразу после 9 класса, сейчас работаю воспитателем в садике!»\n⭐ Данияр, 2022: «Лучшие годы! Преподаватели всегда помогали»\n⭐ Алина, 2024: «Поступила на грант, сейчас учусь и работаю учителем»\n\nХочешь так же? Жми «🎓 Поступление»!",
    "map": "📍 КАК НАС НАЙТИ\n\n🏫 Карагандинский высший гуманитарный колледж\n📍 г. Караганда, пр. Н. Назарбаева, 22\n\nНажми кнопку ниже, чтобы открыть карту 👇",
    "schedule": "📅 РАСПИСАНИЕ\n\nВыбери свою группу 👇",
    "ask": "❓ Напиши свой вопрос одним сообщением!",
    "ask_sent": "✅ Вопрос отправлен!",
    "quiz_start": "🎯 ВИКТОРИНА: Какая специальность тебе подходит?\n\nОтвечай честно! Вопрос 1/3:\n\n❤️ Любишь возиться с маленькими детьми?",
  },
  "kz": {
    "welcome": "👋 Сәлем! Мен Қарағанды жоғары гуманитарлық колледжінің ботымын — ҚГК\n\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 +7 (7212) 41-16-92\n\nТөменнен батырманы таңда 👇",
    "specs": "📚 ҚГК МАМАНДЫҚТАРЫ:\n\n🧒 01120100 — Мектепке дейінгі тәрбие\n📖 01110100 — Бастауыш оқыту педагогикасы\n🎨 01130200 — Қосымша білім беру",
    "admission": "🎓 ОҚУҒА ТҮСУ\n\n📌 Құжаттар:\n• Аттестат (9/11 сынып)\n• Жеке куәлік\n• Фото 3x4 — 4 дана\n• Мед. анықтама 075-У\n\n📅 Қабылдау: 25 маусым — 25 тамыз",
    "pay": "💰 ГРАНТ / ТӨЛЕМ\n\n🎓 Грант: тегін + шәкіртақы\n📞 +7 (7212) 41-16-92",
    "contacts": "📞 БАЙЛАНЫС\n\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 +7 (7212) 41-16-92",
    "news": "📰 ЖАҢАЛЫҚТАР\n\n🎓 2026-2027 оқу жылына қабылдау ашық\n🏫 2026 жылы колледжге — 50 ЖЫЛ!",
    "teachers": "👩‍🏫 БІЗДІҢ ОҚЫТУШЫЛАР\n\n👩‍🏫 Ахметова А.К. — Педагогика, 20 жыл тәжірибе\n👨‍🏫 Серіков Б.М. — Бастауыш оқыту әдістемесі\n👩‍🎨 Омарова Д.С. — Музыка және шығармашылық",
    "reviews": "💬 ТҮЛЕКТЕРДІҢ ПІКІРІ\n\n⭐ Аяулым, 2023: «9-сыныптан кейін түстім, қазір балабақшада жұмыс істеймін!»\n⭐ Данияр, 2022: «Ең жақсы жылдар!»",
    "map": "📍 БІЗДІ ҚАЛАЙ ТАБУҒА БОЛАДЫ\n\n🏫 Қарағанды, Н. Назарбаев даңғылы, 22\n\nКартаны ашу үшін төмендегі батырманы бас 👇",
    "schedule": "📅 САБАҚ КЕСТЕСІ\n\nТобыңды таңда 👇",
    "ask": "❓ Сұрағыңды бір хабарламамен жаз!",
    "ask_sent": "✅ Сұрақ жіберілді!",
    "quiz_start": "🎯 ВИКТОРИНА: Саған қандай мамандық сәйкес келеді?\n\n1/3 сұрақ:\n\n❤️ Кішкентай балалармен ойнағанды жақсы көресің бе?",
  }
}

QUIZ_Q = [
  ("Любишь маленьких детей? / Кішкентай балаларды жақсы көресің бе?", "doshkol"),
  ("Любишь объяснять и учить? / Түсіндіріп, үйреткенді жақсы көресің бе?", "nachal"),
  ("Любишь творчество, музыку, спорт? / Шығармашылықты жақсы көресің бе?", "dop"),
]
QUIZ_RESULT = {
  "ru": {"doshkol": "🧒 Тебе подходит: Дошкольное воспитание! Ты будешь лучшим воспитателем!", "nachal": "📖 Тебе подходит: Учитель начальных классов!", "dop": "🎨 Тебе подходит: Дополнительное образование! Творчество — твое!"},
  "kz": {"doshkol": "🧒 Саған сәйкес: Мектепке дейінгі тәрбие!", "nachal": "📖 Саған сәйкес: Бастауыш сынып мұғалімі!", "dop": "🎨 Саған сәйкес: Қосымша білім беру!"},
}

def lang_of(uid): return user_lang.get(uid, "ru")
def main_menu(lang):
    t = TEXT[lang]
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "ru":
        btns = ["📅 Расписание","📚 Специальности","🎓 Поступление","💰 Гранты","📞 Контакты","📰 Новости","👩‍🏫 Преподаватели","💬 Отзывы","📍 Карта / Как дойти","🎯 Викторина","❓ Задать вопрос","🌐 Язык / Тіл","🌐 Сайт колледжа"]
    else:
        btns = ["📅 Сабақ кестесі","📚 Мамандықтар","🎓 Оқуға түсу","💰 Грант","📞 Байланыс","📰 Жаңалықтар","👩‍🏫 Оқытушылар","💬 Пікірлер","📍 Карта / Қалай жетуге болады","🎯 Викторина","❓ Сұрақ қою","🌐 Тіл / Язык","🌐 Колледж сайты"]
    for i in range(0, len(btns), 2):
        m.add(*[types.KeyboardButton(b) for b in btns[i:i+2]])
    return m

def yes_no_kb(lang):
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang=="ru": m.add(types.KeyboardButton("✅ Да"), types.KeyboardButton("❌ Нет"))
    else: m.add(types.KeyboardButton("✅ Иә"), types.KeyboardButton("❌ Жоқ"))
    return m

def map_kb():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("📍 Открыть в 2ГИС", url="https://2gis.kz/karaganda/search/%D0%9D%D0%B0%D0%B7%D0%B0%D1%80%D0%B1%D0%B0%D0%B5%D0%B2%D0%B0%2022"))
    m.add(types.InlineKeyboardButton("🗺️ Открыть в Яндекс Картах", url="https://yandex.kz/maps/?text=Караганда Назарбаева 22"))
    return m

def schedule_kb(lang):
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("📅 Смотреть расписание на сайте" if lang=="ru" else "📅 Кестені сайттан көру", url=SITE))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    try: bot.send_photo(message.chat.id, PHOTO_URL, caption="ҚГК | КГК")
    except: pass
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇰🇿 Қазақша"))
    bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=m)

@bot.message_handler(func=lambda m: m.text in ["🇷🇺 Русский","🇰🇿 Қазақша","🌐 Язык / Тіл","🌐 Тіл / Язык"])
def set_lang(message):
    if message.text=="🇷🇺 Русский": user_lang[message.chat.id]="ru"
    elif message.text=="🇰🇿 Қазақша": user_lang[message.chat.id]="kz"
    else:
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇰🇿 Қазақша"))
        bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=m); return
    lang=lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["welcome"], reply_markup=main_menu(lang))

# --- НОВЫЕ КНОПКИ ---
@bot.message_handler(func=lambda m: m.text in ["👩‍🏫 Преподаватели","👩‍🏫 Оқытушылар"])
def teachers(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["teachers"], reply_markup=main_menu(lang))

@bot.message_handler(func=lambda m: m.text in ["💬 Отзывы","💬 Пікірлер"])
def reviews(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["reviews"], reply_markup=main_menu(lang))

@bot.message_handler(func=lambda m: m.text in ["📍 Карта / Как дойти","📍 Карта / Қалай жетуге болады"])
def map_h(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["map"], reply_markup=map_kb())

@bot.message_handler(func=lambda m: m.text in ["📅 Расписание","📅 Сабақ кестесі"])
def schedule(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["schedule"], reply_markup=schedule_kb(lang))

@bot.message_handler(func=lambda m: m.text in ["🎯 Викторина"])
def quiz_start(message):
    lang=lang_of(message.chat.id); quiz_state[message.chat.id]=[0, {"doshkol":0,"nachal":0,"dop":0}]
    bot.send_message(message.chat.id, TEXT[lang]["quiz_start"], reply_markup=yes_no_kb(lang))

@bot.message_handler(func=lambda m: m.text in ["✅ Да","❌ Нет","✅ Иә","❌ Жоқ"])
def quiz_answer(message):
    cid=message.chat.id
    if cid not in quiz_state: return
    lang=lang_of(cid); idx, scores = quiz_state[cid]
    if message.text in ["✅ Да","✅ Иә"]:
        scores[QUIZ_Q[idx][1]] += 1
    idx+=1
    if idx>=len(QUIZ_Q):
        best=max(scores, key=scores.get)
        bot.send_message(message.chat.id, "🎉 Результат:\n\n"+QUIZ_RESULT[lang][best], reply_markup=main_menu(lang))
        del quiz_state[cid]
    else:
        quiz_state[cid]=[idx, scores]
        bot.send_message(message.chat.id, f"Вопрос {idx+1}/3:\n\n{QUIZ_Q[idx][0]}", reply_markup=yes_no_kb(lang))

# --- СТАРЫЕ КНОПКИ ---
@bot.message_handler(func=lambda m: m.text in ["📚 Специальности","📚 Мамандықтар"])
def specs(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["specs"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["🎓 Поступление","🎓 Оқуға түсу"])
def adm(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["admission"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["💰 Гранты","💰 Грант"])
def pay(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["pay"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["📞 Контакты","📞 Байланыс"])
def cont(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["contacts"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["📰 Новости","📰 Жаңалықтар"])
def news(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["news"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["🌐 Сайт колледжа","🌐 Колледж сайты"])
def site(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, SITE)
@bot.message_handler(func=lambda m: m.text in ["❓ Задать вопрос","❓ Сұрақ қою"])
def ask_start(message):
    lang=lang_of(message.chat.id); waiting_question.add(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["ask"])
@bot.message_handler(func=lambda m: True)
def other(message):
    lang=lang_of(message.chat.id)
    if message.chat.id in waiting_question:
        waiting_question.remove(message.chat.id)
        try: bot.send_message(ADMIN_ID, f"❓ Вопрос от @{message.from_user.username}:\n\n{message.text}")
        except: pass
        bot.send_message(message.chat.id, TEXT[lang]["ask_sent"], reply_markup=main_menu(lang))
    else:
        bot.send_message(message.chat.id, TEXT[lang]["welcome"], reply_markup=main_menu(lang))

if __name__=="__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()
