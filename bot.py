import os, threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SITE = "https://kgk.mycollege.kz/"
app = Flask(__name__)
@app.route('/')
def home(): return "Bot alive!"
def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
user_lang = {}
waiting = set()

RU_W = "🏫 КАРАГАНДИНСКИЙ ВЫСШИЙ ГУМАНИТАРНЫЙ КОЛЛЕДЖ\n\n🏛 Государственный, с 1976 года, в 2026 нам 50 ЛЕТ!\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 Караганда, пр. Назарбаева, 22\n📞 +7 (7212) 41-16-92\n🏠 Общежитие БЕСПЛАТНО\n\n🎓 2026-2027 УЧЕБНЫЙ ГОД - ПРИЕМ ОТКРЫВАЕТСЯ В ИЮНЕ!\n• Грант + Стипендия 42 000 тг\n• Грантовых мест МНОГО!\n• Можно поступить ОНЛАЙН на OKY платформе\n\n📚 СПЕЦИАЛЬНОСТИ:\n🧒 Дошкольное воспитание\n📖 Начальное обучение\n🇰🇿 Қазақ тілі мұғалімі\n🇬🇧 Ағылшын тілі мұғалімі\n🏃 Дене тәрбиесі мұғалімі\n🎨 Қосымша білім беру\n👩‍🏫 Педагог-ассистент\n🎵 Музыкальное образование\n\n🏆 НАШИ ПОБЕДЫ:\n• 1 место на областном конкурсе молодых педагогов\n• Гран-при фестиваля творчества\n• Лучший колледж города\n\n👩‍🏫 ВЫПУСКНИКИ:\n95% работают в школах и садах Караганды!\nМногие стали директорами школ!\n\n🎉 КРУЖКИ:\nТанцы, вокал, КВН, дебаты, театр, спорт\nВсе бесплатно!\n\nВыбери кнопку ниже 👇"

KZ_W = "🏫 ҚАРАҒАНДЫ ЖОҒАРЫ ГУМАНИТАРЛЫҚ КОЛЛЕДЖІ\n\n🏛 Мемлекеттік, 1976 жылдан, 2026 жылы 50 ЖЫЛ!\n👩‍🏫 Директор: Уатаева Гульмира Султанмуратовна\n📍 Қарағанды, Назарбаев даңғылы, 22\n📞 +7 (7212) 41-16-92\n🏠 Жатақхана ТЕГІН\n\n🎓 2026-2027 оқу жылына қабылдау маусымда ашылады!\n• Грант + Шәкіртақы 42 000 тг\n• Грант орындары КӨП!\n• OKY платформасында ОНЛАЙН түсуге болады\n\n📚 МАМАНДЫҚТАР:\n🧒 Мектепке дейінгі тәрбие\n📖 Бастауыш оқыту\n🇰🇿 Қазақ тілі мұғалімі\n🇬🇧 Ағылшын тілі мұғалімі\n🏃 Дене тәрбиесі мұғалімі\n🎨 Қосымша білім беру\n👩‍🏫 Педагог-ассистент\n🎵 Музыкалық білім\n\n🏆 БІЗДІҢ ЖЕҢІСТЕР:\n• Облыстық жас педагогтар байқауында 1 орын\n• Шығармашылық фестивалінде Гран-при\n• Қаланың үздік колледжі\n\n👩‍🏫 ТҮЛЕКТЕР:\n95% Қарағанды мектептері мен балабақшаларында жұмыс істейді!\nКөбі мектеп директоры болды!\n\n🎉 ҮЙІРМЕЛЕР:\nБи, вокал, КВН, дебат, театр, спорт\nБәрі тегін!\n\nТөменнен батырманы таңда 👇"

RU_S = "📚 СПЕЦИАЛЬНОСТИ:\n\n1. 🧒 Дошкольное воспитание - Воспитатель\n2. 📖 Начальное обучение - Учитель нач. классов\n3. 🇰🇿 Қазақ тілі мұғалімі - Учитель казахского языка\n4. 🇬🇧 Ағылшын тілі мұғалімі - Учитель английского\n5. 🏃 Дене тәрбиесі мұғалімі - Учитель физкультуры\n6. 🎨 Қосымша білім беру - Педагог доп. образования\n7. 👩‍🏫 Педагог-ассистент - Помощник учителя\n8. 🎵 Музыкальное образование - Учитель музыки\n\n🎓 После колледжа - в ВУЗ на 2-3 курс!"
KZ_S = "📚 МАМАНДЫҚТАР:\n\n1. 🧒 Мектепке дейінгі тәрбие - Тәрбиеші\n2. 📖 Бастауыш оқыту - Бастауыш мұғалімі\n3. 🇰🇿 Қазақ тілі мұғалімі\n4. 🇬🇧 Ағылшын тілі мұғалімі\n5. 🏃 Дене тәрбиесі мұғалімі\n6. 🎨 Қосымша білім беру\n7. 👩‍🏫 Педагог-ассистент\n8. 🎵 Музыкалық білім\n\n🎓 Колледжден кейін ЖОО-ға 2-3 курсқа!"

RU_A = "🎓 2026-2027 УЧЕБНЫЙ ГОД - ПРИЕМ ОТКРЫВАЕТСЯ В ИЮНЕ!\n\n📅 На грант: 25 июня - 20 июля\n📅 На платное: 25 июня - 25 августа\n🎓 Грантовых мест МНОГО!\n\n📄 ДОКУМЕНТЫ: Аттестат, удостоверение, фото 3x4 - 4 шт, справка 075-У\n\n📝 КАК ПОСТУПИТЬ:\nМОЖНО ПОСТУПИТЬ ОНЛАЙН НА OKY ПЛАТФОРМЕ!\n1. Зайди на OKY\n2. Выбери КГК\n3. Заполни заявление онлайн\n4. Загрузи документы онлайн\n5. Жди конкурс\n6. Грант - БЕСПЛАТНО + Стипендия 42 000 тг\n\n💻 В колледж приходить НЕ ОБЯЗАТЕЛЬНО!\n\n📞 +7 (7212) 41-16-92"
KZ_A = "🎓 2026-2027 оқу жылына қабылдау маусымда ашылады!\n\n📅 Грантқа: 25 маусым - 20 шілде\n📅 Ақылыға: 25 маусым - 25 тамыз\n🎓 Грант орындары КӨП!\n\n📄 ҚҰЖАТТАР: Аттестат, жеке куәлік, фото 3x4 - 4 дана, анықтама 075-У\n\n📝 ҚАЛАЙ ТҮСЕМІН:\nОНЛАЙН ТҮСУГЕ БОЛАДЫ OKY ПЛАТФОРМАСЫНДА!\n1. OKY-ға кір\n2. ҚЖГК таңда\n3. Өтінішті онлайн толтыр\n4. Құжаттарды онлайн жүкте\n5. Конкурсты күт\n6. Грант - ТЕГІН + Шәкіртақы 42 000 тг\n\n💻 Колледжге келмей-ақ түсе аласың!\n\n📞 +7 (7212) 41-16-92"

RU_P = "💰 ГРАНТ / СТИПЕНДИЯ\n\n• БЕСПЛАТНО\n• Стипендия 42 000 тг каждый месяц\n• Общежитие БЕСПЛАТНО\n• Отличникам - повышенная\n\n📞 +7 (7212) 41-16-92"
KZ_P = "💰 ГРАНТ / ШӘКІРТАҚЫ\n\n• ТЕГІН\n• Шәкіртақы 42 000 тг ай сайын\n• Жатақхана ТЕГІН\n• Үздіктерге - жоғарылатылған\n\n📞 +7 (7212) 41-16-92"

RU_C = "📞 КОНТАКТЫ\n\n📍 Караганда, пр. Назарбаева, 22\n📞 +7 (7212) 41-16-92, 56-12-70\n🕐 Пн-Пт 09:00-18:00\n🏠 Общежитие бесплатно\n📱 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg"
KZ_C = "📞 БАЙЛАНЫС\n\n📍 Қарағанды, Назарбаев даңғылы, 22\n📞 +7 (7212) 41-16-92, 56-12-70\n🕐 Дс-Жм 09:00-18:00\n🏠 Жатақхана тегін\n📱 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg"

RU_N = "📰 НОВОСТИ КОЛЛЕДЖА\n\n🎓 2026-2027 учебный год - прием открывается в ИЮНЕ!\nМожно подать ОНЛАЙН на OKY платформе!\n\n🏫 В 2026 ГОДУ НАМ - 50 ЛЕТ!\nБольшой праздник, концерт, встреча выпускников!\n\n🏆 НАШИ ПОБЕДЫ:\n• 1 место на областном конкурсе молодых педагогов\n• Гран-при фестиваля творчества\n• Лучший колледж города\n\n👩‍🏫 ВЫПУСКНИКИ:\n95% работают в школах и садах Караганды.\nМногие стали директорами!\n\n🎉 СТУДЕНЧЕСКАЯ ЖИЗНЬ:\n• Танцы, вокал, театр\n• КВН, дебаты\n• Волейбол, футбол, теннис\n• Волонтерство\nВсе кружки бесплатно!"
KZ_N = "📰 КОЛЛЕДЖ ЖАҢАЛЫҚТАРЫ\n\n🎓 2026-2027 оқу жылына қабылдау маусымда ашылады!\nOKY платформасында ОНЛАЙН түсуге болады!\n\n🏫 2026 ЖЫЛЫ БІЗГЕ - 50 ЖЫЛ!\nҮлкен мереке, концерт, түлектер кездесуі!\n\n🏆 БІЗДІҢ ЖЕҢІСТЕР:\n• Облыстық жас педагогтар байқауында 1 орын\n• Шығармашылық фестивалінде Гран-при\n• Қаланың үздік колледжі\n\n👩‍🏫 ТҮЛЕКТЕР:\n95% Қарағанды мектептері мен балабақшаларында жұмыс істейді.\nКөбі мектеп директоры болды!\n\n🎉 СТУДЕНТТІК ӨМІР:\n• Би, вокал, театр\n• КВН, дебат\n• Волейбол, футбол, теннис\n• Волонтерлік\nБарлық үйірмелер тегін!"

RU_ST = "🎓 СТУДЕНТТЕРГЕ\n\n📅 Расписание - на сайте\n📝 Сессия: декабрь и май\n💼 Практика в школах и садах\n💰 Стипендия 42 000 тг\n🏠 Общежитие бесплатно\n📚 Библиотека 50 000 книг\n\n🎉 КРУЖКИ - ВСЕ БЕСПЛАТНО:\n• Танцы, вокал, театр\n• КВН, дебаты\n• Волейбол, футбол, теннис"
KZ_ST = "🎓 СТУДЕНТТЕРГЕ\n\n📅 Кесте - сайтта\n📝 Сессия: желтоқсан және мамыр\n💼 Практика мектептерде\n💰 Шәкіртақы 42 000 тг\n🏠 Жатақхана тегін\n📚 Кітапхана 50 000 кітап\n\n🎉 ҮЙІРМЕЛЕР - БӘРІ ТЕГІН:\n• Би, вокал, театр\n• КВН, дебат\n• Волейбол, футбол, теннис"

T = {
 "ru": {"w": RU_W, "s": RU_S, "a": RU_A, "p": RU_P, "c": RU_C, "n": RU_N, "st": RU_ST},
 "kz": {"w": KZ_W, "s": KZ_S, "a": KZ_A, "p": KZ_P, "c": KZ_C, "n": KZ_N, "st": KZ_ST}
}

def lang(uid): return user_lang.get(uid, "ru")
def menu(l):
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if l == "ru":
        m.add(types.KeyboardButton("🏫 О колледже"), types.KeyboardButton("🎓 Студентам"), types.KeyboardButton("📚 Специальности"), types.KeyboardButton("🎓 Поступление"), types.KeyboardButton("💰 Гранты"), types.KeyboardButton("📞 Контакты"), types.KeyboardButton("📰 Новости"), types.KeyboardButton("🌐 Сайт"), types.KeyboardButton("❓ Задать вопрос"), types.KeyboardButton("🌐 Язык"))
    else:
        m.add(types.KeyboardButton("🏫 Колледж туралы"), types.KeyboardButton("🎓 Студенттерге"), types.KeyboardButton("📚 Мамандықтар"), types.KeyboardButton("🎓 Оқуға түсу"), types.KeyboardButton("💰 Грант"), types.KeyboardButton("📞 Байланыс"), types.KeyboardButton("📰 Жаңалықтар"), types.KeyboardButton("🌐 Сайт"), types.KeyboardButton("❓ Сұрақ қою"), types.KeyboardButton("🌐 Тіл"))
    return m

def sm(l):
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("🌐 Сайт", url=SITE))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇰🇿 Қазақша"))
    bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=m)

@bot.message_handler(func=lambda m: m.text in ["🇷🇺 Русский","🇰🇿 Қазақша","🌐 Язык","🌐 Тіл"])
def setlang(message):
    if message.text == "🇷🇺 Русский": user_lang[message.chat.id] = "ru"
    elif message.text == "🇰🇿 Қазақша": user_lang[message.chat.id] = "kz"
    else:
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.add(types.KeyboardButton("🇷🇺 Русский"), types.KeyboardButton("🇰🇿 Қазақша"))
        bot.send_message(message.chat.id, "Выбери язык / Тілді таңда 👇", reply_markup=m)
        return
    l = lang(message.chat.id)
    bot.send_message(message.chat.id, T[l]["w"], reply_markup=menu(l))

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    l = lang(message.chat.id)
    txt = message.text or ""
    if txt in ["🏫 О колледже","🏫 Колледж туралы"]:
        bot.send_message(message.chat.id, T[l]["w"], reply_markup=sm(l))
    elif txt in ["🎓 Студентам","🎓 Студенттерге"]:
        bot.send_message(message.chat.id, T[l]["st"], reply_markup=sm(l))
    elif txt in ["📚 Специальности","📚 Мамандықтар"]:
        bot.send_message(message.chat.id, T[l]["s"], reply_markup=sm(l))
    elif txt in ["🎓 Поступление","🎓 Оқуға түсу"]:
        bot.send_message(message.chat.id, T[l]["a"], reply_markup=sm(l))
    elif txt in ["💰 Гранты","💰 Грант"]:
        bot.send_message(message.chat.id, T[l]["p"], reply_markup=sm(l))
    elif txt in ["📞 Контакты","📞 Байланыс"]:
        bot.send_message(message.chat.id, T[l]["c"], reply_markup=sm(l))
    elif txt in ["📰 Новости","📰 Жаңалықтар"]:
        bot.send_message(message.chat.id, T[l]["n"], reply_markup=sm(l))
    elif txt in ["🌐 Сайт"]:
        bot.send_message(message.chat.id, "🌐 Сайт:\n"+SITE, reply_markup=sm(l))
    elif txt in ["❓ Задать вопрос","❓ Сұрақ қою"]:
        waiting.add(message.chat.id)
        bot.send_message(message.chat.id, "❓ Напиши вопрос!" if l=="ru" else "❓ Сұрағыңды жаз!")
    else:
        t = txt.lower()
        if any(x in t for x in ["қабылдау","маусым","oky","онлайн","прием","поступ","түс","қалай"]):
            bot.send_message(message.chat.id, T[l]["a"], reply_markup=menu(l))
        elif any(x in t for x in ["шәкіртақы","стипенд","грант","төлем","оплата","42000","42 000"]):
            bot.send_message(message.chat.id, T[l]["p"], reply_markup=menu(l))
        elif any(x in t for x in ["мамандық","специальн","мұғалім","учитель","қазақ тілі","ағылшын","дене","ассистент","қосымша"]):
            bot.send_message(message.chat.id, T[l]["s"], reply_markup=menu(l))
        elif any(x in t for x in ["жеңіс","победа","50","түлек","выпуск","квн","дебат","би","вокал","танцы"]):
            bot.send_message(message.chat.id, T[l]["n"], reply_markup=menu(l))
        elif any(x in t for x in ["жатақ","общага","общежит"]):
            bot.send_message(message.chat.id, "🏠 Жатақхана ТЕГІН / Общежитие БЕСПЛАТНО\n📞 +7 (7212) 41-16-92", reply_markup=menu(l))
        elif message.chat.id in waiting:
            waiting.remove(message.chat.id)
            bot.send_message(message.chat.id, "✅ Рахмет! / Спасибо! Сұрағың қабылданды.\n📞 +7 (7212) 41-16-92", reply_markup=menu(l))
        else:
            bot.send_message(message.chat.id, T[l]["w"], reply_markup=menu(l))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Бот запущен...")
    bot.infinity_polling()
