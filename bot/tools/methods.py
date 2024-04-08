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

from telegram import Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from bot.tools.bridge import get_student
from common.parser import parse_snpg
from config import TELEGRAM_TOKEN
from database.engine import session
from database.models import Student

bot = Bot(token=TELEGRAM_TOKEN)


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
        await update.callback_query.edit_message_text(text=old_message, parse_mode='markdown')
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
    student.valid = 1
    session.commit()
    text = f'''
Заявка отправлена:

`
Ф: {surname}
И: {name}
О: {patronymic}
Г: {group}
`
    '''
    old_message = update.callback_query.message.text
    old_message += '\n\nВы: Да, отправить на проверку'
    await update.callback_query.edit_message_text(text=old_message, parse_mode='markdown')
    await bot.send_message(chat_id=update.callback_query.message.chat.id, text=text, parse_mode='markdown')


async def validation_in_process(update) -> None:
    text = 'Ваша заявка уже отправлена'
    await bot.send_message(chat_id=update.effective_user.id, text=text)


async def main_menu(update) -> None:
    applications = session.query(Student).filter_by(valid=1)

    keyboard = [
        [InlineKeyboardButton(text=f'Заявки ({applications.count()})', callback_data='application_list')],
        [InlineKeyboardButton(text='Список участников', callback_data='students_list')],
        [InlineKeyboardButton(text='Турнир', callback_data='tournament')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = '**Главное меню**'

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='markdown')
    else:
        await bot.send_message(chat_id=update.message.chat.id, text=text, reply_markup=reply_markup,
                               parse_mode='markdown')


async def application_list(update) -> None:
    applications = session.query(Student).filter_by(valid=1)

    keyboard = [
        [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
    ]
    for application in applications:
        text = (f'{application.group} '
                f'{application.surname} '
                f'{application.name} '
                f'{application.patronymic[0]}.')
        callback_data = f'application_list_show={application.id}'
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    if len(keyboard) > 10:
        keyboard.append([InlineKeyboardButton(text='В главное меню', callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f'**Всего заявок: {applications.count()}**'

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='markdown')


async def application_list_show(update) -> None:
    student_id = update.callback_query.data.split('=')[1]
    student = session.query(Student).get(student_id)
    keyboard = [
        [
            InlineKeyboardButton(text='Назад', callback_data='application_list')
        ],
        [
            InlineKeyboardButton(text='Отклонить', callback_data=f'application_list_reject={student.id}'),
            InlineKeyboardButton(text='Принять', callback_data=f'application_list_accept={student.id}')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    url = str(student.url)
    surname = str(student.surname)
    name = str(student.name)
    patronymic = str(student.patronymic)
    group = str(student.group)

    text = f'''
<b>ФИО и Группа:</b>
<code>Ф: {surname}
И: {name}
О: {patronymic}
Г: {group}</code>

<b>Telegram:</b>
ID: <code>{student_id}</code>
Tag: @{student.url}
    '''

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')


async def application_list_reject(update) -> None:
    student_id = update.callback_query.data.split('=')[1]
    student = session.query(Student).get(student_id)

    text = f'''
<b>Ваша заявка отклонена:</b>

<code>Ф: {student.surname}
И: {student.name}
О: {student.patronymic}
Г: {student.group}</code>
    '''

    student.surname = ''
    student.name = ''
    student.patronymic = ''
    student.group = ''
    student.valid = 0
    session.commit()

    await bot.send_message(chat_id=student_id, text=text, parse_mode='HTML')
    await application_list(update)


async def application_list_accept(update) -> None:
    student_id = update.callback_query.data.split('=')[1]
    student = session.query(Student).get(student_id)

    keyboard = [
        [
            InlineKeyboardButton(text='В главное меню', callback_data='student_main')
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f'''
<b>Ваша заявка одобрена:</b>

<code>Ф: {student.surname}
И: {student.name}
О: {student.patronymic}
Г: {student.group}</code>
    '''

    student.valid = 2
    session.commit()

    await bot.send_message(chat_id=student_id, text=text, reply_markup=reply_markup, parse_mode='HTML')
    await application_list(update)
    await update_bot_name(update)


async def student_main(update) -> None:
    keyboard = [
        [
            InlineKeyboardButton(text='Турнир', callback_data='?')
        ],
        [
            InlineKeyboardButton(text='Участники', callback_data='?')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = '<b>Главное меню</b>'

    await update.callback_query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')


async def update_bot_name(update) -> None:
    students = session.query(Student).filter_by(valid=2)
    count = students.count()
    name = f'Осталось мест: {64 - count}'
    if count >= 64:
        name = 'Регистрация закрыта'
    await update.get_bot().set_my_name(name=name)
