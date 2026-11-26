import telebot
from telebot import types

TOKEN = "8826297867:AAEJGDvsDhT1c_RIAQrdJUdbuAbtOE2Fz_c"
bot = telebot.TeleBot(TOKEN)

def menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("📚 Расписание", callback_data="rasp"),
        types.InlineKeyboardButton("📢 Новости", callback_data="news"),
        types.InlineKeyboardButton("🎓 Поступление", callback_data="postup"),
        types.InlineKeyboardButton("☎️ Контакты", callback_data="contact"),
        types.InlineKeyboardButton("❓ Вопросы", callback_data="faq")
    )
    m.add(types.InlineKeyboardButton("🌐 Сайт колледжа", url="https://kgk.mycollege.kz/"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎓 Карагандинский высший гуманитарный колледж\n\nВыберите раздел:", reply_markup=menu())

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    bot.answer_callback_query(call.id, text="Загружаю...")
    if call.data == "rasp":
        txt = "📚 Расписание:\nhttps://kgk.mycollege.kz/"
    elif call.data == "news":
        txt = "📢 Новости:\nhttps://kgk.mycollege.kz/"
    elif call.data == "postup":
        txt = "🎓 Поступление\nАттестат, Фото 3x4, Справка 075-У\nhttps://kgk.mycollege.kz/"
    elif call.data == "contact":
        txt = "☎️ Контакты:\n📍 Н. Назарбаева, 22\n📞 (7212) 56-49-33\n📧 krg-koll-6870@bilim09.kz"
    elif call.data == "faq":
        txt = "❓ Вопросы:\nКолледж на Назарбаева 22\nТелефон (7212) 56-49-33"
    else:
        txt = "Выберите раздел"
    bot.send_message(call.message.chat.id, txt, reply_markup=menu())

print("Бот запущен!")
bot.polling(none_stop=True, skip_pending=True)
