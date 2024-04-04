from bot_settings import bot
import sqlite
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
from datetime import datetime


def register_welcome_handlers():
    # commands
    bot.register_message_handler(welcome, commands=['start'])
    bot.register_message_handler(welcome, commands=['menu'])

    # regexp
    bot.register_message_handler(send_products_keyboard, regexp='Выбрать ресторан')
    bot.register_message_handler(welcome, regexp='🔙Назад')
    bot.register_message_handler(send_manager, regexp='💬Менеджер')
    # callback

    bot.register_callback_query_handler(delete_message, lambda call: call.data.startswith('back'))
    bot.register_callback_query_handler(send_rest_info, lambda call: call.data.startswith('send_'))
    bot.register_callback_query_handler(choose_date, lambda call: call.data.startswith('sure_'))
    bot.register_callback_query_handler(number_guests, lambda call: call.data.startswith('choose_time'))
    bot.register_callback_query_handler(choose_time, lambda call: call.data.startswith('number_guests'))
    bot.register_callback_query_handler(final_message, lambda call: call.data.startswith('final'))


def final_message(call):
    name = call.data[11:]
    print(name)
    markup = InlineKeyboardMarkup()
    description, address,map_rest, image = sqlite.get_description_map_by_name(name)
    id_order = 1
    ex = "в обработке"
    rest_id = sqlite.find_rest_id(name)
    print(id_order, ex, call.data[6:11], call.from_user.id, call.data[5], rest_id)
    sqlite.insert_order_to_orders_cache(id_order, ex, call.data[6:11], call.from_user.id, call.data[5], rest_id[0])
    description = f"Заявка сформирована. С вами вскоре свяжется менеджер для потверждения{map_rest}"
    bot.send_message(call.from_user.id, description, reply_markup=markup)


def send_rest_info(call):
    name = call.data[5:]
    description, address, image = sqlite.get_description_by_name(name)
    file = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Збронировать столик", callback_data=f"sure_{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_photo(call.from_user.id, file, description, reply_markup=markup)

def choose_date(call):
    name = call.data[5:]
    description, address, image = sqlite.get_description_by_name(name)
    file = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"05.04", callback_data=f"choose_time05/04{name}"))
    markup.add(InlineKeyboardButton(text=f"06.04", callback_data=f"choose_time06/04{name}"))
    markup.add(InlineKeyboardButton(text=f"07.04", callback_data=f"choose_time07/04{name}"))
    markup.add(InlineKeyboardButton(text=f"08.04", callback_data=f"choose_time08/04{name}"))
    markup.add(InlineKeyboardButton(text=f"09.04", callback_data=f"choose_time09/04{name}"))
    markup.add(InlineKeyboardButton(text=f"10.04", callback_data=f"choose_time10/04{name}"))
    markup.add(InlineKeyboardButton(text=f"11.04", callback_data=f"choose_time11/04{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_message(call.from_user.id, "Выберите дату", reply_markup=markup)

def number_guests(call):
    name = call.data[16:]
    tmp = call.data[11:16]
    description, address, image = sqlite.get_description_by_name(name)
    file = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"1", callback_data=f"final1{tmp}{name}"))
    markup.add(InlineKeyboardButton(text=f"2", callback_data=f"final2{tmp}{name}"))
    markup.add(InlineKeyboardButton(text=f"3", callback_data=f"final3{tmp}{name}"))
    markup.add(InlineKeyboardButton(text=f"4", callback_data=f"final4{tmp}{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_message(call.from_user.id, "Выберите количество гстей", reply_markup=markup)

def choose_time(call):
    name = call.data[10:]
    number = call.data[10]
    description, address, image = sqlite.get_free_time(name,number)
    image = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"забронировать", callback_data=f"ChooseTime{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_photo(call.from_user.id, image, description, reply_markup=markup)


def send_products_keyboard(message, edit=False):
    image = open(f'images/welcome.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="FARШ Кирочная ул. 17", callback_data="send_FARШ"))
    markup.add(InlineKeyboardButton(text="Leth Набережной реки Фонтанки, 82.", callback_data="send_Leth"))
    markup.add(InlineKeyboardButton(text="Mekong Садовая ул., 42", callback_data="send_Mekong"))
    text = ("Mint Table Reservation - это многофункциональный бот, который поможет быстро и удобно забронировать столик в "
            "любимом ресторане. Наш бот упрощает процесс бронирования и делает его доступным в любое время дня и ночи.")
    bot.send_photo(message.from_user.id, image, text, reply_markup=markup)


def send_manager(message):
    text = '[Написать менеджеру](https://t.me/gisubo)'
    bot.send_message(message.from_user.id, text, parse_mode='markdown')


def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def welcome(message):
    sqlite.insert_user(message.from_user.id, message.from_user.first_name)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Выбрать ресторан"),  KeyboardButton(text="💬Менеджер"))
    bot.send_message(message.from_user.id, "Приветствую тебя в нашей сети ресторанов", reply_markup=markup)

