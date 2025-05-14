import os
import telebot
from replace_text import replace_text_in_docx
from get_pattern_message import get_pattern_message
from telebot import types
import re
import shutil

API_TOKEN = '7937646870:AAH1f-_vPaebCHVtl6VLit1YBMizY82JNl0'  
bot = telebot.TeleBot(API_TOKEN)

pattern_file_IP = 'Pattern/ИП 2024 Шаблон Договор №00-00 Контекстная реклама'
pattern_file_OOO = 'Pattern/ООО 2024 Шаблон Договор №00-00 Контекстная реклама'
pattern_file2 = 'Pattern/2024 Шаблон Приложение 1 (00-00) Разработка'
pattern_file3 = 'Pattern/2024 Шаблон Приложение 2 (00-00) Ведение'
pattern_file4_IP = 'Pattern/верн Доп. соглашение к договору 1'
pattern_file4_OOO = 'Pattern/пример Доп.соглашение к Договору'

photoIP = [
    'Photo/Choice_1/List1.jpg',
    'Photo/Choice_1/List2.jpg',
    'Photo/Choice_1/List3.jpg',
    'Photo/Choice_1/List4.jpg',
    'Photo/Choice_1/List5.jpg',
    'Photo/Choice_1/List6.jpg',
    'Photo/Choice_1/List7.jpg'
]
photoOOO = [
    'Photo/Choice_2/List1.jpg',
    'Photo/Choice_2/List2.jpg',
    'Photo/Choice_2/List3.jpg',
    'Photo/Choice_2/List4.jpg',
    'Photo/Choice_2/List5.jpg',
    'Photo/Choice_2/List6.jpg',
    'Photo/Choice_2/List7.jpg'
]
photo2 = 'Photo/Pattern_2/List1.png'
photo3 = 'Photo/Pattern_3/List1.png'
photo4_IP = 'Photo/Pattern_4/List1.jpg'
photo4_OOO = 'Photo/Pattern_4/List2.jpg'

manul = """Добро пожаловать в PatternBot! 🎉 Этот бот предназначен для удобного заполнения шаблонов договоров через Telegram. Данный бот поддерживает различные типы договоров и предоставляет пользователям простой интерфейс для ввода необходимых данных. Давайте разберем, как начать работу с ботом и какие функции он предлагает.

Как начать работу с ботом:
1️⃣Выбор шаблона:

В главном меню вы можете выбрать нужный шаблон документа, нажав на соответствующую кнопку. Доступные шаблоны включают:
Договор размещения рекламы📕
Разработка рекламы📙
Введение рекламы📗
Доп. соглашение к договору📘
   
Заполнение данных:

После выбора шаблона вам будет предложено ввести данные в соответствии с запрашиваемыми полями. Убедитесь, что формат данных соответствует требованиям (например, номер договора, дата, ФИО и т.д.).
Бот предоставит формат, который нужно скопировать без названия "📜Формат:" и заполнить. Например так:
 
📜Формат:
1.Номер договора: 01-25
2.Дата: 01.01.2025
3.Стоимоcть: 15000   
4.Должность заказчика: ИП Никитин Н.И
5.Полное ФИО заказчика: Никитин Никита Иванович

2️⃣Получение документа:

После успешного заполнения шаблона бот отправит вам готовый документ в формате .docx.

3️⃣Ошибки ввода:

Если вы допустите ошибку при вводе данных, бот сообщит о ней и предложит ввести данные заново. Например, если вы введете номер договора в неправильном формате, бот укажет на ошибку и предложит отправить исправленное сообщение заново.

4️⃣Возврат в меню:

Если вы хотите вернуться в главное меню, просто нажмите кнопку "Вернуться в меню".

5️⃣Пример работы с ботом:

Вы запускаете бота и видите главное меню.
Вы выбираете "Договор размещения рекламы📕".
Затем выбираете "ИП" или "ООО".
Бот предоставляет вам формат для заполнения.
Вы вводите данные в соответствии с форматом и отправляете их боту.
Бот проверяет данные, и если все в порядке, отправляет вам готовый документ.

6️⃣Дополнительные опции:

Нажав на кнопку 'Инструкция📒' вы снова можете ознакомиться с данным путеводителем еще раз.
"""

# старт
@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = bot.send_message(message.chat.id, manul)
    bot.pin_chat_message(message.chat.id, welcome_message.message_id)
    show_main_menu(message.chat.id)


user_states = {}
processing_active = {}
states = {}

def clear_state(chat_id):
    """Очищает состояние пользователя."""
    if chat_id in states:
        del states[chat_id]

def set_user_state(chat_id, state):
    user_states[chat_id] = state
    processing_active[chat_id] = True
def clear_user_state(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]
    processing_active[chat_id] = False

def get_user_state_inside(chat_id):
    try:
        print(user_states[chat_id])
        if user_states[chat_id] is not None:
            return user_states[chat_id]
    except:
        print("тут пусто :(")

# основное меню
def show_main_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Договор размещения рекламы📕', callback_data='menu_choice'))
    keyboard.add(types.InlineKeyboardButton('Разработка рекламы📙', callback_data='Pattern2'))
    keyboard.add(types.InlineKeyboardButton('Введение рекламы📗', callback_data='Pattern3'))
    keyboard.add(types.InlineKeyboardButton('Доп. соглашение к договору📘', callback_data='menu_choice1'))
    keyboard.add(types.InlineKeyboardButton('Инструкция📒', callback_data='show_manual'))
    bot.send_message(chat_id, "Выберите интересующий вас шаблон:", reply_markup=keyboard)

def menu_choice(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('ИП', callback_data='Choice1'))
    keyboard.add(types.InlineKeyboardButton('ООО', callback_data='Choice2'))
    keyboard.add(types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu'))
    bot.send_message(chat_id, "Выберите интересующую вас часть:", reply_markup=keyboard)

def menu_choice1(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('ИП', callback_data='Choice_1'))
    keyboard.add(types.InlineKeyboardButton('ООО', callback_data='Choice_2'))
    keyboard.add(types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu'))
    bot.send_message(chat_id, "Выберите интересующую вас часть:", reply_markup=keyboard)

# переходы через callback_data
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    # Убедимся, что состояние для chat_id существует
    if chat_id not in states:
        states[chat_id] = {}

    if call.data == 'main_menu':
        states[chat_id] = {"main_menu": False, "Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                           "Pattern2": False, "Pattern3": False, "Pattern4": False}
        states[chat_id]["main_menu"] = True
        name_file = get_user_state_inside(chat_id)
        try:
            if "new_file_path" in name_file:
                try:
                    os.remove(name_file.get('new_file_path'))
                except:
                    print("файл удален, упс")
        except:
            print("тут тоже пусто ;(")
        clear_user_state(chat_id)  
        processing_active[chat_id] = False  
        show_main_menu(chat_id)

        
    elif call.data.startswith('Pattern'):
        states[chat_id] = {"Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                        "Pattern2": False, "Pattern3": False, "Pattern4": False}
        clear_user_state(chat_id)  
        set_user_state(chat_id, call.data)  

        process_document_name(chat_id)
    
    elif call.data == 'show_manual':
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu'))
        
        # Отправляем инструкцию с клавиатурой
        bot.send_message(chat_id, manul, reply_markup=keyboard)

    if call.data == 'menu_choice':
        states[chat_id] = {"Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                        "Pattern2": False, "Pattern3": False, "Pattern4": False}
        clear_user_state(chat_id)  
        menu_choice(chat_id)
    elif call.data.startswith('Choice') and not call.data.startswith('Choice_'):
        states[chat_id] = {"Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                        "Pattern2": False, "Pattern3": False, "Pattern4": False}
        clear_user_state(chat_id)  
        set_user_state(chat_id, call.data) 

        process_document_name(chat_id)

    if call.data == 'menu_choice1':
        states[chat_id] = {"Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                        "Pattern2": False, "Pattern3": False, "Pattern4": False}
        clear_user_state(chat_id)  
        menu_choice1(chat_id)
    elif call.data.startswith('Choice_'):
        states[chat_id] = {"Choice1": False, "Choice2": False,
                           "Choice_1": False, "Choice_2": False,
                        "Pattern2": False, "Pattern3": False, "Pattern4": False}
        clear_user_state(chat_id)  
        set_user_state(chat_id, call.data) 

        process_document_name(chat_id)

# Универсальные ошибки
def validate_input(pattern, line, expected_type, line_number):
    if expected_type == "номер":
        if not re.match(r'^\d{2}-\d{2}', line):
            return f"Ошибка в строке {line_number}: Номер должен быть в формате 00-00."
    elif expected_type == "дата":
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}', line):
            return f"Ошибка в строке {line_number}: Дата должна быть в формате дд.мм.гггг."
    elif expected_type == "стоимость":
        if not re.match(r'^\d+(\.\d{1,2})?', line):
            return f"Ошибка в строке {line_number}: Стоимость должна быть числом (например, 1000 или 1000.00)."
    elif expected_type == "текст":
        if pattern == 'Choice1' and not line:
            return None
        if not line:
            if line_number != 17:
                return f"Ошибка в строке {line_number}: Это поле не может быть пустым."
    elif expected_type == "ФИО":
        if not re.match(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+', line):
            return f"Ошибка в строке {line_number}: ФИО должно содержать три части (фамилия, имя, отчество)."
    return None

# Вывод названия для удобства
def get_message_for_pattern(chat_id):
    pattern = user_states.get(chat_id)
    if pattern == 'Choice1':
        return 'Pattern/Договор размещения рекламы'
    elif pattern == 'Choice2':
        return 'Pattern/Договор размещения рекламы'
    elif pattern == 'Pattern2':
        return 'Pattern/Приложение1 разработка рекламы'
    elif pattern == 'Pattern3':
        return 'Pattern/Приложение2 введение рекламы'
    if pattern == 'Choice_1':
        return 'Pattern/ИП доп. соглашение к договору'
    elif pattern == 'Choice_2':
        return 'Pattern/доп. соглашение к договору'

# Вывод названия исходника
def get_message_for_exodus_pattern(chat_id):
    pattern = user_states.get(chat_id)
    if pattern == 'Choice1':
        return pattern_file_IP + '.docx'
    elif pattern == 'Choice2':
        return pattern_file_OOO + '.docx'
    elif pattern == 'Pattern2':
        return pattern_file2 + '.docx'
    elif pattern == 'Pattern3':
        return pattern_file3 + '.docx'
    if pattern == 'Choice_1':
        return pattern_file4_IP + '.docx'
    elif pattern == 'Choice_2':
        return pattern_file4_OOO + '.docx'

def def_old_info_list(chat_id):
    if user_states != {}:
        pattern = user_states.get(chat_id)
        pattern = pattern["pattern"]
    else:
        pattern = slovar.get(chat_id)
        pattern = pattern["pattern"]
    if pattern == 'Choice1':
        old_info_list = ["description", "Name_site", "NumberAgreement", "full_date", "<ФИО>", 
                        "<Юридический адрес>", "PhysicalAddress", "<ОГРНИП>", "<ИНН>", 
                        "<Банковские реквизиты>", "<р/с>", "<к/с>", "<БИК>", "<Телефон>", "email"]
        return old_info_list
    elif pattern == 'Choice2':
        old_info_list = ["description", "Name_site", "NumberAgreement", "full_date", "<ООО -устав>", "post",
                        "FIO", "<Юридический адрес>", "PhysicalAddress", "<ОГРНИП>", "<ИНН>", 
                        "<Банковские реквизиты>", "<р/с>", "<к/с>", "<БИК>", "<Телефон>", "email"]
        return old_info_list
    elif pattern == 'Pattern2':
        old_info_list = ["<Номер договора>", "<Дата>", "<Цена>", "post", "full_name"]
        return old_info_list
    elif pattern == 'Pattern3':
        old_info_list = ["NumberAgreement", "<Дата>", "<Цена>", "post", "full_name"]
        return old_info_list
    elif pattern == 'Choice_1':
        old_info_list = ["Povod", "NumberAgreement", "Agr", "<Атад>", "<Дата>",
                         "ОГРНИП", "FIO", "Price", "<Энтри>"]
        return old_info_list
    elif pattern == 'Choice_2':
        old_info_list = ["Povod", "NumberAgreement", "Agr", "<Атад>", "<Дата>", 
                        "Organization", "OST", "FIO", "Price", "<Энтри>"]
        return old_info_list

# Вывод формата шаблона с фотками
def send_template(chat_id, keyboard):
    if user_states != {}:
        pattern = user_states.get(chat_id)
        pattern = pattern["pattern"]
    else:
        pattern = slovar.get(chat_id)
        pattern = pattern["pattern"]
    if pattern == 'Choice1':
        media = [types.InputMediaPhoto(types.InputFile(photo_path)) for photo_path in photoIP]
        bot.send_media_group(chat_id, media)
        message = bot.send_message(chat_id, text=get_pattern_message(pattern), reply_markup=keyboard)
    if pattern == 'Choice2':
        media = [types.InputMediaPhoto(types.InputFile(photo_path)) for photo_path in photoOOO]
        bot.send_media_group(chat_id, media)
        message = bot.send_message(chat_id, text=get_pattern_message(pattern), reply_markup=keyboard)
    elif pattern == 'Pattern2':
        message = bot.send_photo(chat_id, photo=open(photo2, 'rb'), caption=get_pattern_message(pattern), reply_markup=keyboard)
    elif pattern == 'Pattern3':
        message = bot.send_photo(chat_id, photo=open(photo3, 'rb'), caption=get_pattern_message(pattern), reply_markup=keyboard)
    elif pattern == 'Choice_1':
        message = bot.send_photo(chat_id, photo=open(photo4_IP, 'rb'), caption=get_pattern_message(pattern), reply_markup=keyboard)
    elif pattern == 'Choice_2':
        message = bot.send_photo(chat_id, photo=open(photo4_OOO, 'rb'), caption=get_pattern_message(pattern), reply_markup=keyboard)
    return message

def process_document_name(chat_id):
    print(user_states)
    pattern = user_states.get(chat_id)
    states[chat_id][pattern] = True
    states[chat_id]["main_menu"] = False

    # Проверяем, не вернулся ли пользователь в меню
    if not processing_active.get(chat_id, False):
        return

    # Определяем путь к исходному файлу в зависимости от выбранного шаблона
    template_file = get_message_for_exodus_pattern(chat_id)
    new_file_path = get_message_for_pattern(chat_id)

    # Копируем файл с новым именем
    try:
        print("Ориг. название: ", template_file)
        print("Новое название: ", new_file_path)
        shutil.copy(template_file, f'{new_file_path}.docx')
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при копировании файла: {str(e)}")
        return
    
    # Сохраняем путь к новому файлу в состоянии пользователя
    user_states[chat_id] = {'pattern': pattern, 'new_file_path': new_file_path}
    print(user_states)

    # Выводим шаблон для заполнения
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_back = telebot.types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu')
    keyboard.add(btn_back)

    # Отправляем шаблон в зависимости от выбранного паттерна
    message = send_template(chat_id, keyboard)
    bot.register_next_step_handler(message, filling_out_the_document)

slovar = {}

def filling_out_the_document(message):
    chat_id = message.chat.id

    # Проверяем, не вернулся ли пользователь в меню
    if not processing_active.get(chat_id, False):
        print("Пользователь, вышел")
        return

    try:
        dict_text = user_states[chat_id]
        new_file_path = dict_text["new_file_path"]
        pattern = dict_text["pattern"]
        
        slovar[chat_id] = {'pattern': pattern, 'new_file_path': new_file_path}
    except:
        print(user_states)

    if processing_active.get(chat_id, False):
        old_info_list = def_old_info_list(chat_id)
        clear_user_state(chat_id)  # Сбрасываем состояние после завершения ввода
        dict_text = slovar[chat_id]
        new_file_path = dict_text["new_file_path"]
        pattern = dict_text["pattern"]

        user_input = message.text
        if user_input is None or user_input.strip() == "":
            text = "Повторите запрос снова."
            send_pattern_message(chat_id, text)
            return
        
        lines = user_input.split('\n')
        new_info_list = []
        error_messages = []

        # Определяем ожидаемые параметры и типы в зависимости от шаблона
        if pattern == 'Choice1':
            expected_count = 15
            expected_types = ["текст", "текст", "номер", "дата", "ФИО", "текст", "текст", "текст",
                            "текст", "текст", "текст", "текст", "текст", "текст", "текст"]
        elif pattern == 'Choice2':
            expected_count = 17
            expected_types = ["текст", "текст", "номер", "дата", "текст", "текст", "ФИО", "текст",
                                "текст", "текст", "текст", "текст", 
                                "текст", "текст", "текст", "текст", "текст"]
        elif pattern == 'Pattern2':
            expected_count = 5
            expected_types = ["номер", "дата", "стоимость", "текст", "ФИО"]
        elif pattern == 'Pattern3':
            expected_count = 5
            expected_types = ["номер", "дата", "стоимость", "текст", "ФИО"]
        elif pattern == 'Choice_1':
            expected_count = 9
            expected_types = ["текст", "текст", "номер", "дата", "дата", "текст", "ФИО", "стоимость", "дата"]
        elif pattern == 'Choice_2':
            expected_count = 10
            expected_types = ["текст", "текст", "номер", "дата", "дата", "текст", "текст", "ФИО", "ФИО от лица", "стоимость", "дата"]

        # Проверяем, что количество введенных параметров совпадает с ожидаемым
        if pattern.startswith("Choice"):
            if len(lines) == (expected_count - 1) or len(lines) == expected_count:
                for i, line in enumerate(lines):
                    if ":" in line:
                        colon_index = line.index(":")
                        info = line[colon_index + 1:].strip()

                        new_info_list.append(info)

                        error_message = validate_input(pattern, info, expected_types[i], i + 1)
                        if error_message:
                            error_messages.append(error_message)
                    else:
                        error_messages.append(f"Текст не соответствует формату шаблона.❌")
                        break
            else:
                error_messages.append(f"Ожидается {expected_count} параметров, но было введено {len(lines)}.❌")
        elif pattern.startswith('Pattern'):
            if len(lines) != expected_count:
                error_messages.append(f"Ожидается {expected_count} параметров, но было введено {len(lines)}.❌")
            else:
                for i, line in enumerate(lines):
                    if ":" in line:
                        colon_index = line.index(":")
                        info = line[colon_index + 1:].strip()  # Убираем пробелы после двоеточия

                        new_info_list.append(info)

                        error_message = validate_input(pattern, info, expected_types[i], i + 1)
                        if error_message:
                            error_messages.append(error_message)
                    else:
                        error_messages.append(f"Текст не соответствует формату шаблона.❌")
                        break

        print(new_file_path)
        if error_messages:
            print("Внутри states:", states)
            print("Внутри user_states:", user_states)
            if (states[chat_id].get("main_menu") != True):
                processing_active[chat_id] = True
                error_messages.append("Повторите попытку")
                send_pattern_message(chat_id, "\n".join(error_messages))
                bot.register_next_step_handler(message, filling_out_the_document)
        else:
            try:
                print(old_info_list, "/n")
                print(new_info_list, "/n")
                print(new_file_path, old_info_list, new_info_list, pattern)
                new_document_name = replace_text_in_docx(new_file_path, old_info_list, new_info_list, pattern)
                if new_document_name == "ошибка":
                    print("Внутри states:", states)
                    print("Внутри user_states:", user_states)
                    if (states[chat_id].get("main_menu") != True):
                        processing_active[chat_id] = True
                        send_pattern_message(chat_id, f"Пожалуйста введите название организации в «».❌")
                        bot.register_next_step_handler(message, filling_out_the_document)
                else:
                    with open(new_document_name, "rb") as doc_file:
                        bot.send_document(message.chat.id, doc_file)
                        bot.register_next_step_handler(message, filling_out_the_document)
                    if pattern == 'Choice1':    
                        send_pattern_message(chat_id, f'Договор ИП Контекстная реклама размещения рекламы был заполнен.✅')
                    elif pattern == 'Choice2':
                        send_pattern_message(chat_id, f'ООО Договор размещения контекстной рекламы был заполнен.✅')
                    elif pattern == 'Pattern2':
                        send_pattern_message(chat_id, f'Приложение 1 Разработка рекламы было заполнено.✅')
                    elif pattern == 'Pattern3':
                        send_pattern_message(chat_id, f'Приложение 2 Введение рекламы было заполнено.✅')
                    elif pattern == 'Choice_1':
                        send_pattern_message(chat_id, f'ИП доп. соглашение к договору было заполнено.✅')
                    elif pattern == 'Choice_2':
                        send_pattern_message(chat_id, f'ООО доп. соглашение к договору было заполнено.✅')
            except Exception as e:
                send_pattern_message(chat_id, f"Произошла ошибка при обработке документа: {str(e)}")
            finally:
                # Удалите файл, если он существует
                if os.path.exists(new_document_name):
                    try:
                        os.remove(new_document_name)  # Удалите файл только после его закрытия
                    except Exception as e:
                        bot.send_message(chat_id, f"Ошибка при удалении файла: {str(e)}")  

# возврат в меню
def send_pattern_message(chat_id, text):
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_back = telebot.types.InlineKeyboardButton("Вернуться в меню↩️", callback_data='main_menu')
    keyboard.add(btn_back)
    bot.send_message(chat_id, text, reply_markup=keyboard)

# запуск
if __name__ == '__main__':
    bot.polling(none_stop=True)