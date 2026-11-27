import os,threading,telebot
from telebot import types
from flask import Flask
TOKEN=os.environ.get("BOT_TOKEN")
bot=telebot.TeleBot(TOKEN)
SITE="https://kgk.mycollege.kz/"
ADMIN=123456789
app=Flask(__name__)
@app.route('/')
def h(): return "OK"
threading.Thread(target=lambda:app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000))),daemon=True).start()
U={};WQ=set();WO=set();Q={}
def L(u): return U.get(u,"ru")
D={
"ru":{
"w":"👋 Привет! Я бот ҚЖГК\n🏫 Қарағанды жоғары гуманитарлық колледжі\n🎓 С 1976 года — 50 ЛЕТ в 2026!\n📍 Назарбаева, 22\n📞 8(7212)41-16-92\n📞 8(7212)56-12-70\n📞 8(7212)56-05-40",
"a":"🏫 О КОЛЛЕДЖЕ — ҚЖГК\n📅 1976 год, в 2026 — 50 ЛЕТ!\n👩‍🎓 Выпускников: 10 000+\n👩‍🏫 Преподавателей: 40+\n🏫 Кабинеты, актовый зал, спортзал, библиотека 30 000 книг, столовая, общежитие, кабинеты Көркем еңбек\n🌟 Почему ҚЖГК? 1) После 9 и 11 кл. 2) ГРАНТ+стипендия 3) Сразу работа в школе/садике 4) В ВУЗ без ЕНТ 5) КВН, концерты, TikTok @gumlife_krg\n📍 Назарбаева, 22 📞 41-16-92 | 56-12-70 | 56-05-40",
"s":"📚 СПЕЦИАЛЬНОСТИ ҚЖГК:\n🧒 01120100 Дошкольное воспитание — Воспитатель, от 180 000 тг\n📖 01110100 Учитель начальных классов — от 220 000 тг\n🎨 01130200 Доп. образование — Педагог кружков, вожатый\n🎨 КӨРКЕМ ЕҢБЕК — Учитель худ. труда, рукоделия, дизайна\nНе знаешь? Жми 🎯 Викторина!",
"p":"🎓 ПОСТУПЛЕНИЕ ҚЖГК 2026-2027\nПосле 9 и 11 кл., БЕЗ ЕНТ!\n📄 Аттестат, удостоверение, фото 3x4-4шт, справка 075-У\n📅 Грант: 25.06-15.07, Платно: 25.06-25.08\n📍 Назарбаева, 22, каб.101 📞 41-16-92 | 56-12-70 | 56-05-40",
"g":"💰 ГРАНТ ҚЖГК\n🎓 БЕСПЛАТНО + стипендия! Нужен средний балл от 4.0\n💡 Лайфхак: учишься на 4-5 один семестр — переведешься на грант!\n📞 41-16-92",
"c":"📞 КОНТАКТЫ ҚЖГК\n📍 Назарбаева, 22\n📞 8(7212)41-16-92\n📞 8(7212)56-12-70\n📞 8(7212)56-05-40\n🕐 Пн-Пт 09:00-18:00\n🚍 Автобусы: 01,07,19,29,45",
"n":"📰 НОВОСТИ ҚЖГК\n🎓 Набор 2026-2027 открыт!\n🎉 В 2026 нам 50 ЛЕТ!\n🎨 Неделя Көркем еңбек\n🏆 1 место «Лучший воспитатель»\nInstagram @gumanitaricollegeinkrg",
"t":"👩‍🏫 ПРЕПОДАВАТЕЛИ ҚЖГК\nАхметова А.К. — Педагогика\nСериков Б.М. — Начальное обучение\nОмарова Д.С. — Музыка\n🎨 Көркем еңбек мұғалімі — Худ. труд, рукоделие, дизайн\nКалиева Н.Т. — Психология",
"r":"💬 ОТЗЫВЫ ҚЖГК\n⭐ Аяулым: «На грант, сейчас воспитатель, 200 000 тг»\n⭐ Данияр: «Лучшие 4 года!»\n⭐ Алина, Көркем еңбек: «Научилась шить, веду свой кружок!»",
"m":"📍 ҚЖГК — Назарбаева, 22\n🚍 Автобусы: 01,07,19,29,45\nНажми кнопку ниже 👇",
"sc":"📅 РАСПИСАНИЕ ҚЖГК\n1 пара: 08:30-10:00\n2 пара: 10:10-11:40\n3 пара: 12:00-13:30\nОбед 13:30-14:00\n4 пара: 14:00-15:30",
"so":"📱 СОЦСЕТИ ҚЖГК\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg\n📘 Facebook: Карагандинский гуманитарный колледж",
"ph":"📸 НАШ КОЛЛЕДЖ ҚЖГК\nКабинеты, актовый зал, спортзал, столовая!",
"o":"🎓 ДЕНЬ ОТКРЫТЫХ ДВЕРЕЙ ҚЖГК\n📍 Назарбаева, 22\n📅 Каждая суббота 11:00\nНапиши Имя и телефон. Пример: Аяулым 87071234567",
"od":"✅ Ты записан(а) в ҚЖГК! Ждем в субботу 11:00! 🎉",
"ask":"❓ Напиши свой вопрос одним сообщением!",
"ad":"✅ Вопрос отправлен в ҚЖГК!",
"dor":"🏠 ОБЩЕЖИТИЕ ҚЖГК\n✅ Есть для иногородних!\n🛏️ Комнаты 2-3 чел, кухня, душ\n📍 5 мин от колледжа 📞 41-16-92",
"life":"🎉 СТУДЕНЧЕСКАЯ ЖИЗНЬ ҚЖГК\n🎤 КВН, концерты 💃 Танцы, вокал 🎨 Кружок Көркем еңбек ⚽ Футбол, волейбол 📱 TikTok @gumlife_krg",
"q":"🎯 ВИКТОРИНА ҚЖГК\nВопрос 1/3: Любишь маленьких детей?"},
"kz":{
"w":"👋 Сәлем! Мен ҚЖГК ботымын\n🏫 Қарағанды жоғары гуманитарлық колледжі\n🎓 1976 жылдан — 2026 жылы 50 ЖЫЛ!\n📍 Назарбаев, 22\n📞 8(7212)41-16-92\n📞 8(7212)56-12-70\n📞 8(7212)56-05-40",
"a":"🏫 КОЛЛЕДЖ ТУРАЛЫ — ҚЖГК\n📅 1976 жыл, 2026 жылы — 50 ЖЫЛ!\n👩‍🎓 Түлектер: 10 000+\n🏫 Кабинеттер, акт залы, спортзал, 30 000 кітапты кітапхана, асхана, жатақхана, Көркем еңбек кабинеттері\n🌟 Неге ҚЖГК? 1) 9-11 сыныптан 2) ГРАНТ+шәкіртақы 3) Бірден жұмыс 4) ҰБТ-сыз ЖОО 5) КВН, TikTok @gumlife_krg",
"s":"📚 ҚЖГК МАМАНДЫҚТАРЫ:\n🧒 01120100 Мектепке дейінгі тәрбие — Тәрбиеші, 180 000 тг-ден\n📖 01110100 Бастауыш оқыту — Мұғалім\n🎨 01130200 Қосымша білім\n🎨 КӨРКЕМ ЕҢБЕК — Көркем еңбек мұғалімі",
"p":"🎓 ҚЖГК-ҒА ТҮСУ 2026-2027\n9 және 11 сыныптан, ҰБТ-сыз!\n📄 Аттестат, жеке куәлік, фото 3x4-4дана, анықтама 075-У\n📅 Грант: 25.06-15.07, Ақылы: 25.06-25.08\n📍 Назарбаев, 22, 101-кабинет 📞 41-16-92",
"g":"💰 ГРАНТ ҚЖГК\n🎓 ТЕГІН + шәкіртақы! Орташа балл 4.0-ден жоғары\n💡 1 семестрді 4-5-ке оқысаң грантқа ауысуға болады!",
"c":"📞 БАЙЛАНЫС ҚЖГК\n📍 Назарбаев, 22\n📞 8(7212)41-16-92\n📞 8(7212)56-12-70\n📞 8(7212)56-05-40",
"n":"📰 ЖАҢАЛЫҚТАР ҚЖГК\n🎓 2026-2027 қабылдау ашық!\n🎉 2026 жылы 50 ЖЫЛ!",
"t":"👩‍🏫 ОҚЫТУШЫЛАР ҚЖГК\nАхметова А.К. — Педагогика\n🎨 Көркем еңбек мұғалімі — Көркем еңбек, қолөнер",
"r":"💬 ПІКІРЛЕР ҚЖГК\n⭐ Аяулым: «Грантқа түстім, қазір тәрбиешімін!»",
"m":"📍 ҚЖГК — Назарбаев, 22",
"sc":"📅 САБАҚ КЕСТЕСІ ҚЖГК\n1 жұп: 08:30-10:00\n2 жұп: 10:10-11:40",
"so":"📱 ӘЛЕУМЕТТІК ЖЕЛІЛЕР ҚЖГК\n📸 Instagram: @gumanitaricollegeinkrg\n🎵 TikTok: @gumlife_krg",
"ph":"📸 БІЗДІҢ КОЛЛЕДЖ ҚЖГК",
"o":"🎓 АШЫҚ ЕСІК КҮНІ ҚЖГК\n📍 Назарбаев, 22\n📅 Әр сенбі 11:00\nАты-жөніңді және телефоныңды жаз. Мысалы: Аяулым 87071234567",
"od":"✅ Сен ҚЖГК-ға жазылдың! Сенбі 11:00-де күтеміз! 🎉",
"ask":"❓ Сұрағыңды бір хабарламамен жаз!",
"ad":"✅ Сұрақ ҚЖГК-ға жіберілді!",
"dor":"🏠 ЖАТАҚХАНА ҚЖГК\n✅ Басқа қаладан келгендерге бар!\n📍 Колледждің жанында",
"life":"🎉 СТУДЕНТТІК ӨМІР ҚЖГК\n🎤 КВН, концерттер 🎨 Көркем еңбек үйірмесі 📱 TikTok @gumlife_krg",
"q":"🎯 ВИКТОРИНА ҚЖГК\n1/3 сұрақ: Кішкентай балаларды жақсы көресің бе?"}
}
M={"🏫 О колледже":"a","🏫 Колледж туралы":"a","📚 Специальности":"s","📚 Мамандықтар":"s","🎓 Поступление":"p","🎓 Оқуға түсу":"p","💰 Гранты":"g","💰 Грант":"g","📞 Контакты":"c","📞 Байланыс":"c","📰 Новости":"n","📰 Жаңалықтар":"n","👩‍🏫 Преподаватели":"t","👩‍🏫 Оқытушылар":"t","💬 Отзывы":"r","💬 Пікірлер":"r","📍 Карта / Как дойти":"m","📍 Карта / Қалай жетуге болады":"m","📅 Расписание":"sc","📅 Сабақ кестесі":"sc","📱 Соцсети":"so","📱 Әлеуметтік желілер":"so","📸 Фото колледжа":"ph","📸 Колледж фотосы":"ph","🏠 Общежитие":"dor","🏠 Жатақхана":"dor","🎉 Студенческая жизнь":"life","🎉 Студенттік өмір":"life"}
def menu(l):
    m=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    b=["🏫 О колледже","📚 Специальности","🎓 Поступление","💰 Гранты","📅 Расписание","📞 Контакты","📰 Новости","👩‍🏫 Преподаватели","💬 Отзывы","📍 Карта / Как дойти","📸 Фото колледжа","🎓 День открытых дверей","🎯 Викторина","📱 Соцсети","🏠 Общежитие","🎉 Студенческая жизнь","❓ Задать вопрос","🌐 Язык / Тіл","🌐 Сайт колледжа"] if l=="ru" else ["🏫 Колледж туралы","📚 Мамандықтар","🎓 Оқуға түсу","💰 Грант","📅 Сабақ кестесі","📞 Байланыс","📰 Жаңалықтар","👩‍🏫 Оқытушылар","💬 Пікірлер","📍 Карта / Қалай жетуге болады","📸 Колледж фотосы","🎓 Ашық есік күні","🎯 Викторина","📱 Әлеуметтік желілер","🏠 Жатақхана","🎉 Студенттік өмір","❓ Сұрақ қою","🌐 Тіл / Язык","🌐 Колледж сайты"]
    for i in range(0,len(b),2): m.add(*[types.KeyboardButton(x) for x in b[i:i+2]])
    return m
def kb(url,txt):
    k=types.InlineKeyboardMarkup(); k.add(types.InlineKeyboardButton(txt,url=url)); return k
@bot.message_handler(commands=['start'])
def st(m):
    k=types.ReplyKeyboardMarkup(resize_keyboard=True); k.add(types.KeyboardButton("🇷🇺 Русский"),types.KeyboardButton("🇰🇿 Қазақша")); bot.send_message(m.chat.id,"Выбери язык / Тілді таңда 👇",reply_markup=k)
@bot.message_handler(func=lambda m: m.text in ["🇷🇺 Русский","🇰🇿 Қазақша","🌐 Язык / Тіл","🌐 Тіл / Язык"])
def lg(m):
    if m.text=="🇷🇺 Русский": U[m.chat.id]="ru"
    elif m.text=="🇰🇿 Қазақша": U[m.chat.id]="kz"
    else: st(m); return
    bot.send_message(m.chat.id,D[L(m.chat.id)]["w"],reply_markup=menu(L(m.chat.id)))
@bot.message_handler(func=lambda m: m.text in M)
def info(m):
    l=L(m.chat.id); k=M[m.text]
    if k=="m": bot.send_message(m.chat.id,D[l][k],reply_markup=kb("https://2gis.kz/karaganda/search/Назарбаева%2022","📍 Открыть в 2ГИС"))
    elif k=="so":
        kk=types.InlineKeyboardMarkup(); kk.add(types.InlineKeyboardButton("📸 Instagram",url="https://instagram.com/gumanitaricollegeinkrg")); kk.add(types.InlineKeyboardButton("🎵 TikTok @gumlife_krg",url="https://www.tiktok.com/@gumlife_krg")); kk.add(types.InlineKeyboardButton("📘 Facebook",url="https://www.facebook.com/share/1BX3xK3aRa/")); bot.send_message(m.chat.id,D[l][k],reply_markup=kk)
    elif k=="ph": bot.send_message(m.chat.id,D[l][k]+"\n📸 https://instagram.com/gumanitaricollegeinkrg\n🎵 https://www.tiktok.com/@gumlife_krg")
    elif k=="sc": bot.send_message(m.chat.id,D[l][k],reply_markup=kb(SITE,"📅 Смотреть на сайте"))
    else: bot.send_message(m.chat.id,D[l][k],reply_markup=menu(l))
@bot.message_handler(func=lambda m: m.text in ["🎓 День открытых дверей","🎓 Ашық есік күні"])
def op(m): WO.add(m.chat.id); bot.send_message(m.chat.id,D[L(m.chat.id)]["o"])
@bot.message_handler(func=lambda m: m.chat.id in WO)
def ops(m):
    l=L(m.chat.id); WO.remove(m.chat.id)
    try: bot.send_message(ADMIN,f"🎓 ЗАПИСЬ День открытых дверей от @{m.from_user.username}:\n{m.text}")
    except: pass
    bot.send_message(m.chat.id,D[l]["od"],reply_markup=menu(l))
@bot.message_handler(func=lambda m: m.text in ["🎯 Викторина"])
def qs(m): Q[m.chat.id]=[0,{"d":0,"n":0,"t":0}]; k=types.ReplyKeyboardMarkup(resize_keyboard=True); k.add(types.KeyboardButton("✅ Да"),types.KeyboardButton("❌ Нет")); bot.send_message(m.chat.id,D[L(m.chat.id)]["q"],reply_markup=k)
@bot.message_handler(func=lambda m: m.text in ["✅ Да","❌ Нет","✅ Иә","❌ Жоқ"])
def qa(m):
    c=m.chat.id
    if c not in Q: return
    l=L(c); i,s=Q[c]
    if m.text in ["✅ Да","✅ Иә"]: s[list(s.keys())[i]]+=1
    i+=1
    if i>=3:
        b=max(s,key=s.get); r={"d":"🧒 Тебе подходит: Дошкольное воспитание!","n":"📖 Тебе подходит: Учитель начальных классов!","t":"🎨 Тебе подходит: Доп. образование / Көркем еңбек!"}[b] if l=="ru" else {"d":"🧒 Саған: Мектепке дейінгі тәрбие!","n":"📖 Саған: Бастауыш мұғалімі!","t":"🎨 Саған: Қосымша білім / Көркем еңбек!"}[b]
        bot.send_message(c,"🎉 "+r,reply_markup=menu(l)); del Q[c]
    else: Q[c]=[i,s]; qs2=["Любишь объяснять и учить?","Любишь творчество?"] if l=="ru" else ["Түсіндіріп үйреткенді жақсы көресің бе?","Шығармашылықты жақсы көресің бе?"]; k=types.ReplyKeyboardMarkup(resize_keyboard=True); k.add(types.KeyboardButton("✅ Да"),types.KeyboardButton("❌ Нет")); bot.send_message(c,f"Вопрос {i+1}/3: {qs2[i-1]}",reply_markup=k)
@bot.message_handler(func=lambda m: m.text in ["🌐 Сайт колледжа","🌐 Колледж сайты"])
def site(m): bot.send_message(m.chat.id,SITE)
@bot.message_handler(func=lambda m: m.text in ["❓ Задать вопрос","❓ Сұрақ қою"])
def ask(m): WQ.add(m.chat.id); bot.send_message(m.chat.id,D[L(m.chat.id)]["ask"])
@bot.message_handler(func=lambda m: True)
def all(m):
    l=L(m.chat.id)
    if m.chat.id in WQ:
        WQ.remove(m.chat.id)
        try: bot.send_message(ADMIN,f"❓ Вопрос от @{m.from_user.username}:\n{m.text}")
        except: pass
        bot.send_message(m.chat.id,D[l]["ad"],reply_markup=menu(l))
    else: bot.send_message(m.chat.id,D[l]["w"],reply_markup=menu(l))
bot.infinity_polling()
