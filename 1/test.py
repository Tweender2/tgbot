# import telebot
# from telebot import types

# API_TOKEN = '7937646870:AAH1f-_vPaebCHVtl6VLit1YBMizY82JNl0'  # Замените на ваш API токен
# bot = telebot.TeleBot(API_TOKEN)

# user_states = {}
# processing_active = {}

# def set_user_state(chat_id, state):
#     user_states[chat_id] = state
#     processing_active[chat_id] = True

# def clear_user_state(chat_id):
#     if chat_id in user_states:
#         del user_states[chat_id]
#     processing_active[chat_id] = False

# @bot.message_handler(commands=['start'])
# def start(message):
#     show_main_menu(message.chat.id)

# def show_main_menu(chat_id):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton('Договор размещения рекламы📕', callback_data='menu_choice'))
#     keyboard.add(types.InlineKeyboardButton('Разработка рекламы📙', callback_data='Pattern2'))
#     keyboard.add(types.InlineKeyboardButton('Введение рекламы📗', callback_data='Pattern3'))
#     keyboard.add(types.InlineKeyboardButton('Доп. соглашение к договору📘', callback_data='Pattern4'))
#     bot.send_message(chat_id, "Добро пожаловать, выберите интересующий вас шаблон:", reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: True)
# def handle_query(call):
#     chat_id = call.message.chat.id
#     if call.data == 'main_menu':
#         clear_user_state(chat_id)
#         show_main_menu(chat_id)
#     elif call.data.startswith('Pattern'):
#         clear_user_state(chat_id)  # Сбрасываем состояние пользователя перед обработкой нового выбора
#         set_user_state(chat_id, call.data)  # Установка состояния для текущего шаблона
        
#         keyboard = types.InlineKeyboardMarkup()
#         btn_back = types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu')
#         keyboard.add(btn_back)
#         bot.send_message(chat_id, "Пожалуйста, введите новое название документа:", reply_markup=keyboard)
        
#         # Регистрация обработчика следующего шага
#         print(call.data, processing_active.get(chat_id))
#         bot.register_next_step_handler(call.message, process_document_name)

# def process_document_name(message):
#     chat_id = message.chat.id
#     pattern = user_states.get(chat_id)  # Получаем текущий шаблон из состояния пользователя

#     print(pattern, processing_active.get(chat_id))
#     if processing_active.get(chat_id, False):
#         clear_user_state(chat_id)  # Сбрасываем состояние после завершения ввода
#         bot.send_message(chat_id, f'Вы ввели: {message.text} {pattern}')

# if __name__ == "__main__":
#     bot.polling(none_stop=True)

import telebot
from telebot import types

API_TOKEN = '7937646870:AAH1f-_vPaebCHVtl6VLit1YBMizY82JNl0'
bot = telebot.TeleBot(API_TOKEN)

user_states = {}  # Словарь для хранения состояний пользователей

@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = "Добро пожаловать! Пожалуйста, выберите опцию."
    markup = types.InlineKeyboardMarkup()
    btn_name = types.InlineKeyboardButton("Ввод имени", callback_data="input_name")
    btn_surname = types.InlineKeyboardButton("Ввод фамилии", callback_data="input_surname")
    markup.add(btn_name, btn_surname)
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["input_name", "input_surname"])
def ask_for_input(call):
    user_states[call.message.chat.id] = call.data  # Сохраняем состояние пользователя
    prompt = "Пожалуйста, введите " + ("имя:" if call.data == "input_name" else "фамилию:")
    markup = types.InlineKeyboardMarkup()
    btn_menu = types.InlineKeyboardButton("Вернуться в меню", callback_data="return_to_menu")
    markup.add(btn_menu)
    bot.send_message(call.message.chat.id, prompt, reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_input(message):
    user_input = message.text
    if len(user_input) > 10:
        text = "Ошибка: введенное значение слишком длинное. Пожалуйста, введите менее 10 символов."
        # Добавляем кнопку "Вернуться в меню"
        markup = types.InlineKeyboardMarkup()
        btn_menu = types.InlineKeyboardButton("Вернуться в меню", callback_data="return_to_menu")
        markup.add(btn_menu)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        return  # Ожидаем новый ввод от пользователя

    # Если пользователь ввел корректное значение, можем сохранить или обработать его
    name_or_surname = user_states[message.chat.id]
    text = f"Спасибо! Вы ввели {'имя' if name_or_surname == 'input_name' else 'фамилию'}: {user_input}"
    del user_states[message.chat.id]  # Удаляем состояние пользователя

    # Предлагаем вернуться в главное меню
    markup = types.InlineKeyboardMarkup()
    btn_menu = types.InlineKeyboardButton("Вернуться в меню", callback_data="return_to_menu")
    markup.add(btn_menu)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "return_to_menu")
def return_to_menu(call):
    start(call.message)  # Возвращаемся к стартовому сообщению

if __name__ == '__main__':
    bot.polling(none_stop=True)


