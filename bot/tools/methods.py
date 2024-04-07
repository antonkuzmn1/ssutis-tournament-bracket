"""

Copyright 2024 Anton Kuzmin (https://github.com/antonkuzmn1)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import json

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from telegram import Bot
from bot.tools.bridge import get_student
from common.parser import parse_snpg
from config import TELEGRAM_TOKEN
from database.engine import session

bot = Bot(token=TELEGRAM_TOKEN)

# await update.get_bot().set_my_name(name='ssutis_bot')


async def request_snpg(update) -> None:
    text = '''
Введите ваше ФИО и группу.

Пример:
Иванов Иван Иванович АА-111
Иванов Иван АА-111 (если нет отчества)
    '''
    # print(json.dumps(update.to_dict(), ensure_ascii=False, indent=4))
    if update.message:
        await update.message.reply_text(text=text)
    else:
        old_message = update.callback_query.message.text
        old_message += '\n\nВы: Нет, заполнить заново'
        await update.callback_query.edit_message_text(text=old_message)
        await bot.send_message(chat_id=update.callback_query.message.chat.id, text=text)


async def confirm_snpg(update) -> None:
    keyboard = [
        [InlineKeyboardButton(text="Да, отправить на проверку", callback_data='request_validation')],
        [InlineKeyboardButton(text="Нет, заполнить заново", callback_data='request_snpg')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    parsed_snpg = parse_snpg(update.message.text)
    surname = parsed_snpg['surname']
    name = parsed_snpg['name']
    patronymic = parsed_snpg['patronymic']
    group = parsed_snpg['group']

    if surname == '':
        await request_snpg(update)
        return

    text = f'''
Вот ваши данные:

`
Ф: {surname}
И: {name}
О: {patronymic}
Г: {group}
`

Всё корректно определилось?
    '''

    await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='markdown')


async def request_validation(update) -> None:
    depth1 = update.callback_query.message.text.split('\n')
    surname = depth1[3].split(': ')[1]
    name = depth1[4].split(': ')[1]
    patronymic = depth1[5].split(': ')[1]
    group = depth1[6].split(': ')[1]
    student = get_student(update)
    student.surname = surname
    student.name = name
    student.patronymic = patronymic
    student.group = group
    session.commit()
    text = f'''
Заявка отправлена:

Ф: {surname}
И: {name}
О: {patronymic}
Г: {group}
    '''
    old_message = update.callback_query.message.text
    old_message += '\n\nВы: Да, отправить на проверку'
    await update.callback_query.edit_message_text(text=update.callback_query.message.text)
    await bot.send_message(chat_id=update.callback_query.message.chat.id, text=text)


async def validation_in_process(update) -> None:
    text = 'Ваша заявка уже отправлена'
    await bot.send_message(chat_id=update.effective_user.id, text=text)


def main_menu(update, student):
    var = None
    student.location = 'main'

    if student.valid:
        return
    else:
        keyboard = [[InlineKeyboardButton("Изменить параметры", callback_data="set_params")]]

        if all([student.surname, student.name, student.patronymic, student.group]):
            keyboard.append([InlineKeyboardButton("Отправить заявку", callback_data="pizda")])

        message = f'''
        **Главное меню**
    
        - Вы не являетесь подтвержденным пользователем.
        - Неподтвержденные пользователи не могут принять участие в турнире.
        - Чтоб исправить положение необходимо заполнить пустые поля ниже и отправить заявку на регистрацию.
        - Для заполнения полей используйте кнопки под этим сообщением.
        - Кнопка для отправки заявки появится если все поля будут заполнены.
        
        `
        Ф: {student.surname}
        И: {student.name}
        О: {student.patronymic}
        Г: {student.group}
        `
        '''

        update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='markdown')
