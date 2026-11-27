import os, threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SITE = "https://kgk.mycollege.kz/"
ADMIN_ID = 123456789  # <-- ВСТАВЬ СВОЙ ID
PHOTO_URL = "https://i.postimg.cc/XXXXXXXX/photo.jpg"

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

user_lang = {}
waiting_question = set()
waiting_openday = set()
quiz_state = {}

TEXT = {
  "ru": {
    "welcome": "👋 Привет! Я бот Карагандинского высшего гуманитарного колледжа — КГК\n\n🏫 С 1976 года готовим учителей и воспитателей\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40\n\nВыбери кнопку ниже 👇",
    "about": "🏫 О КОЛЛЕДЖЕ — КГК\n\nКарагандинский высший гуманитарный колледж — один из лучших педагогических колледжей Караганды!\n\n📅 Основан: 1976 год\n🎓 В 2026 году нам — 50 ЛЕТ!\n👩‍🎓 Выпускников: более 10 000\n👩‍🏫 Преподавателей: 40+\n\n🎯 Наша цель: готовить лучших учителей и воспитателей для Казахстана!\n\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "specs": "📚 СПЕЦИАЛЬНОСТИ КГК:\n\n🧒 01120100 — Дошкольное воспитание\n📖 01110100 — Педагогика начального обучения\n🎨 01130200 — Доп. образование\n🎨 Көркем еңбек — Художественный труд",
    "admission": "🎓 ПОСТУПЛЕНИЕ\n\n📌 Документы:\n• Аттестат (9/11 кл.)\n• Удостоверение личности\n• Фото 3x4 — 4 шт\n• Мед. справка 075-У\n\n📅 Прием: 25 июня — 25 августа\n🎓 Есть ГРАНТ!\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "pay": "💰 ГРАНТЫ / ОПЛАТА\n\n🎓 Грант: бесплатно + стипендия\n💳 Платно: уточняй в приемной\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "contacts": "📞 КОНТАКТЫ КГК\n\n📍 г. Караганда, пр. Н. Назарбаева, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40\n🕐 Пн-Пт 09:00 — 18:00",
    "news": "📰 НОВОСТИ\n\n🎓 Открыт набор на 2026-2027 учебный год\n🏫 В 2026 году колледжу — 50 ЛЕТ!",
    "teachers": "👩‍🏫 НАШИ ПРЕПОДАВАТЕЛИ\n\n👩‍🏫 Ахметова А.К. — Педагогика, 20 лет опыта\n👨‍🏫 Сериков Б.М. — Методика начального обучения\n👩‍🎨 Омарова Д.С. — Музыка и творчество\n🎨 Көркем еңбек мұғалімі — Художественный труд и рукоделие\n👩‍🏫 Калиева Н.Т. — Психология и дошкольное воспитание\n\nВсе преподаватели — с высшим образованием и большим опытом!",
    "reviews": "💬 ОТЗЫВЫ ВЫПУСКНИКОВ\n\n⭐ Аяулым, 2023: «Поступила сразу после 9 класса, сейчас работаю воспитателем в садике!»\n⭐ Данияр, 2022: «Лучшие годы! Преподаватели всегда помогали»\n⭐ Алина, 2024: «Поступила на грант, сейчас учусь и работаю учителем»\n\nХочешь так же? Жми «🎓 Поступление»!",
    "map": "📍 КАК НАС НАЙТИ\n\n🏫 Карагандинский высший гуманитарный колледж\n📍 г. Караганда, пр. Н. Назарбаева, 22\n\nНажми кнопку ниже, чтобы открыть карту 👇",
    "schedule": "📅 РАСПИСАНИЕ\n\nРасписание смотри на сайте колледжа 👇",
    "social": "📱 НАШИ СОЦСЕТИ\n\nПодпишись, там все новости и жизнь колледжа 👇\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg\n📘 Facebook: Карагандинский гуманитарный колледж",
    "photo": "📸 НАШ КОЛЛЕДЖ\n\n🏫 Современные кабинеты, актовый зал, спортзал, столовая!\n\nСмотри фото и видео ниже 👇",
    "openday": "🎓 ДЕНЬ ОТКРЫТЫХ ДВЕРЕЙ\n\nПриходи посмотреть колледж вживую!\n📍 Назарбаева, 22\n📅 Каждая суббота в 11:00\n\nЧтобы записаться, напиши своё Имя и номер телефона одним сообщением.\nНапример: Аяулым 87071234567",
    "openday_done": "✅ Ты записан(а) на День открытых дверей!\n\nМы тебе позвоним и напомним. Ждем тебя в субботу в 11:00! 🎉",
    "ask": "❓ Напиши свой вопрос одним сообщением!",
    "ask_sent": "✅ Вопрос отправлен!",
    "quiz_start": "🎯 ВИКТОРИНА: Какая специальность тебе подходит?\n\nОтвечай честно! Вопрос 1/3:\n\n❤️ Любишь возиться с маленькими детьми?",
  },
  "kz": {
    "welcome": "👋 Сәлем! Мен Қарағанды жоғары гуманитарлық колледжінің ботымын — ҚГК\n\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40\n\nТөменнен батырманы таңда 👇",
    "about": "🏫 КОЛЛЕДЖ ТУРАЛЫ — ҚГК\n\nҚарағанды жоғары гуманитарлық колледжі — Қарағандының үздік педагогикалық колледждерінің бірі!\n\n📅 Құрылған: 1976 жыл\n🎓 2026 жылы бізге — 50 ЖЫЛ!\n👩‍🎓 Түлектер: 10 000-нан астам\n\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "specs": "📚 ҚГК МАМАНДЫҚТАРЫ:\n\n🧒 01120100 — Мектепке дейінгі тәрбие\n📖 01110100 — Бастауыш оқыту педагогикасы\n🎨 01130200 — Қосымша білім беру\n🎨 Көркем еңбек",
    "admission": "🎓 ОҚУҒА ТҮСУ\n\n📌 Құжаттар:\n• Аттестат (9/11 сынып)\n• Жеке куәлік\n• Фото 3x4 — 4 дана\n• Мед. анықтама 075-У\n\n📅 Қабылдау: 25 маусым — 25 тамыз\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "pay": "💰 ГРАНТ / ТӨЛЕМ\n\n🎓 Грант: тегін + шәкіртақы\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "contacts": "📞 БАЙЛАНЫС\n\n📍 Қарағанды қ., Н. Назарбаев даңғылы, 22\n📞 8 (7212) 41-16-92\n📞 8 (7212) 56-12-70\n📞 8 (7212) 56-05-40",
    "news": "📰 ЖАҢАЛЫҚТАР\n\n🎓 2026-2027 оқу жылына қабылдау ашық\n🏫 2026 жылы колледжге — 50 ЖЫЛ!",
    "teachers": "👩‍🏫 БІЗДІҢ ОҚЫТУШЫЛАР\n\n👩‍🏫 Ахметова А.К. — Педагогика, 20 жыл тәжірибе\n👨‍🏫 Серіков Б.М. — Бастауыш оқыту әдістемесі\n👩‍🎨 Омарова Д.С. — Музыка және шығармашылық\n🎨 Көркем еңбек мұғалімі — Көркем еңбек және қолөнер",
    "reviews": "💬 ТҮЛЕКТЕРДІҢ ПІКІРІ\n\n⭐ Аяулым, 2023: «9-сыныптан кейін түстім, қазір балабақшада жұмыс істеймін!»\n⭐ Данияр, 2022: «Ең жақсы жылдар!»",
    "map": "📍 БІЗДІ ҚАЛАЙ ТАБУҒА БОЛАДЫ\n\n🏫 Қарағанды, Н. Назарбаев даңғылы, 22\n\nКартаны ашу үшін төмендегі батырманы бас 👇",
    "schedule": "📅 САБАҚ КЕСТЕСІ\n\nКестені колледж сайтынан көр 👇",
    "social": "📱 БІЗДІҢ ӘЛЕУМЕТТІК ЖЕЛІЛЕР\n\nЖазыл, барлық жаңалық сол жерде 👇\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg",
    "photo": "📸 БІЗДІҢ КОЛЛЕДЖ\n\n🏫 Заманауи кабинеттер, акт залы, спортзал, асхана!\n\nФото мен видеоны төменнен көр 👇",
    "openday": "🎓 АШЫҚ ЕСІК КҮНІ\n\nКолледжді тірі көр!\n📍 Назарбаев, 22\n📅 Әр сенбі сағат 11:00\n\nЖазылу үшін аты-жөніңді және телефоныңды бір хабарламамен жаз.\nМысалы: Аяулым 87071234567",
    "openday_done": "✅ Сен Ашық есік күніне жазылдың!\n\nСаған хабарласамыз. Сенбі күні сағат 11:00-де күтеміз! 🎉",
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
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "ru":
        btns = ["🏫 О колледже","📚 Специальности","🎓 Поступление","💰 Гранты","📅 Расписание","📞 Контакты","📰 Новости","👩‍🏫 Преподаватели","💬 Отзывы","📍 Карта / Как дойти","📸 Фото колледжа","🎓 День открытых дверей","🎯 Викторина","📱 Соцсети","❓ Задать вопрос","🌐 Язык / Тіл","🌐 Сайт колледжа"]
    else:
        btns = ["🏫 Колледж туралы","📚 Мамандықтар","🎓 Оқуға түсу","💰 Грант","📅 Сабақ кестесі","📞 Байланыс","📰 Жаңалықтар","👩‍🏫 Оқытушылар","💬 Пікірлер","📍 Карта / Қалай жетуге болады","📸 Колледж фотосы","🎓 Ашық есік күні","🎯 Викторина","📱 Әлеуметтік желілер","❓ Сұрақ қою","🌐 Тіл / Язык","🌐 Колледж сайты"]
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

def social_kb():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("📸 Instagram @gumanitaricollegeinkrg", url="https://instagram.com/gumanitaricollegeinkrg"))
    m.add(types.InlineKeyboardButton("🎵 TikTok @gumlife_krg", url="https://www.tiktok.com/@gumlife_krg"))
    m.add(types.InlineKeyboardButton("📘 Facebook", url="https://www.facebook.com/share/1BX3xK3aRa/"))
    m.add(types.InlineKeyboardButton("🌐 Сайт колледжа", url=SITE))
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

@bot.message_handler(func=lambda m: m.text in ["🏫 О колледже","🏫 Колледж туралы"])
def about_h(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["about"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["📱 Соцсети","📱 Әлеуметтік желілер"])
def social_h(message):
    lang=lang_of(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["social"], reply_markup=social_kb())
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
@bot.message_handler(func=lambda m: m.text in ["📸 Фото колледжа","📸 Колледж фотосы"])
def photo_h(message):
    lang=lang_of(message.chat.id)
    bot.send_message(message.chat.id, TEXT[lang]["photo"])
    try:
        bot.send_message(message.chat.id, "📸 Наши фото в Instagram:\nhttps://instagram.com/gumanitaricollegeinkrg\n🎵 Видео в TikTok:\nhttps://www.tiktok.com/@gumlife_krg")
    except: pass
@bot.message_handler(func=lambda m: m.text in ["🎓 День открытых дверей","🎓 Ашық есік күні"])
def openday_start(message):
    lang=lang_of(message.chat.id); waiting_openday.add(message.chat.id); bot.send_message(message.chat.id, TEXT[lang]["openday"])
@bot.message_handler(func=lambda m: m.chat.id in waiting_openday)
def openday_save(message):
    lang=lang_of(message.chat.id); waiting_openday.remove(message.chat.id)
    try: bot.send_message(ADMIN_ID, f"🎓 НОВАЯ ЗАПИСЬ на День открытых дверей!\n\nОт: @{message.from_user.username}\nДанные: {message.text}")
    except: pass
    bot.send_message(message.chat.id, TEXT[lang]["openday_done"], reply_markup=main_menu(lang))
@bot.message_handler(func=lambda m: m.text in ["🎯 Викторина"])
def quiz_start(message):
    lang=lang_of(message.chat.id); quiz_state[message.chat.id]=[0, {"doshkol":0,"nachal":0,"dop":0}]
    bot.send_message(message.chat.id, TEXT[lang]["quiz_start"], reply_markup=yes_no_kb(lang))
@bot.message_handler(func=lambda m: m.text in ["✅ Да","❌ Нет","✅ Иә","❌ Жоқ"])
def quiz_answer(message):
    cid=message.chat.id
    if cid not in quiz_state: return
    lang=lang_of(cid); idx, scores = quiz_state[cid]
    if message.text in ["✅ Да","✅ Иә"]: scores[QUIZ_Q[idx][1]] += 1
    idx+=1
    if idx>=len(QUIZ_Q):
        best=max(scores, key=scores.get)
        bot.send_message(message.chat.id, "🎉 Результат:\n\n"+QUIZ_RESULT[lang][best], reply_markup=main_menu(lang))
        del quiz_state[cid]
    else:
        quiz_state[cid]=[idx, scores]
        bot.send_message(message.chat.id, f"Вопрос {idx+1}/3:\n\n{QUIZ_Q[idx][0]}", reply_markup=yes_no_kb(lang))
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
    bot.send_message(message.chat.id, SITE)
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
