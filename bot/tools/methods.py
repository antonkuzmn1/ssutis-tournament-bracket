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

from bot.tools.bridge import get_student
from bot.tools.timeout import check
from common.parser import parse_snpg
from config import TELEGRAM_TOKEN
from database.engine import SESSION
from database.models import Student

_BOT = Bot(token=TELEGRAM_TOKEN)


async def request_snpg(update) -> None:
    """
    view
    :param update:
    :return: 
    """
    _TEXT: str = '''
Введите ваше ФИО и группу.

Пример:
Иванов Иван Иванович АА-111
Иванов Иван АА-111 (если нет отчества)
    '''
    # print(json.dumps(update.to_dict(), ensure_ascii=False, indent=4))
    if update.message:
        await update.message.reply_text(text=_TEXT)
    else:
        old_message = update.callback_query.message._TEXT
        old_message += '\n\nВы: Нет, заполнить заново'
        await update.callback_query.edit_message_text(text=old_message, parse_mode='markdown')
        await _BOT.send_message(chat_id=update.callback_query.message.chat.id, text=_TEXT)


async def confirm_snpg(update) -> None:
    """
    view
    :param update: 
    :return: 
    """
    _KEYBOARD = [
        [InlineKeyboardButton(text="Да, отправить на проверку", callback_data='request_validation')],
        [InlineKeyboardButton(text="Нет, заполнить заново", callback_data='request_snpg')],
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _PARSED_SNPG = parse_snpg(update.message._TEXT)
    _SURNAME: str = _PARSED_SNPG['surname']
    _NAME: str = _PARSED_SNPG['name']
    _PATRONYMIC: str = _PARSED_SNPG['patronymic']
    _GROUP: str = _PARSED_SNPG['group']

    if _SURNAME == '':
        await request_snpg(update)
        return

    _TEXT: str = f'''
Вот ваши данные:

`
Ф: {_SURNAME}
И: {_NAME}
О: {_PATRONYMIC}
Г: {_GROUP}
`

Всё корректно определилось?
    '''

    await update.message.reply_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='markdown')


async def request_validation(update) -> None:
    """
    view
    :param update: 
    :return: 
    """

    _DEPTH1 = update.callback_query.message._TEXT.split('\n')
    _SURNAME: str = _DEPTH1[3].split(': ')[1]
    _NAME: str = _DEPTH1[4].split(': ')[1]
    _PATRONYMIC: str = _DEPTH1[5].split(': ')[1]
    _GROUP: str = _DEPTH1[6].split(': ')[1]

    student = get_student(update)
    student.surname = _SURNAME
    student.name = _NAME
    student.patronymic = _PATRONYMIC
    student.group = _GROUP
    student.valid = 1
    SESSION.commit()

    _TEXT: str = f'''
Заявка отправлена:

`
Ф: {_SURNAME}
И: {_NAME}
О: {_PATRONYMIC}
Г: {_GROUP}
`
    '''

    old_message: str = update.callback_query.message._TEXT
    old_message += '\n\nВы: Да, отправить на проверку'
    await update.callback_query.edit_message_text(text=old_message, parse_mode='markdown')
    await _BOT.send_message(chat_id=update.callback_query.message.chat.id, text=_TEXT, parse_mode='markdown')


async def validation_in_process(update) -> None:
    """
    view
    :param update:
    :return:
    """
    if check(update):
        _TEXT = 'Ваша заявка уже отправлена'
        await _BOT.send_message(chat_id=update.effective_user.id, text=_TEXT)


async def main_menu(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _REQUESTS = SESSION.query(Student).filter_by(valid=1)

    _KEYBOARD = [
        [InlineKeyboardButton(text=f'Заявки ({_REQUESTS.count()})', callback_data='application_list')],
        [InlineKeyboardButton(text='Список участников', callback_data='students_list')],
        [InlineKeyboardButton(text='Турнир', callback_data='tournament')],
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _TEXT: str = '**Главное меню**'

    if update.callback_query:
        await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='markdown')
    else:
        await _BOT.send_message(chat_id=update.message.chat.id, text=_TEXT, reply_markup=_REPLY_MARKUP,
                                parse_mode='markdown')


async def application_list(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _REQUESTS = SESSION.query(Student).filter_by(valid=1)

    _keyboard = [
        [InlineKeyboardButton(text='В главное меню', callback_data='main_menu')]
    ]
    for _REQUEST in _REQUESTS:
        _TEXT: str = (f'{_REQUEST.group} '
                      f'{_REQUEST.surname} '
                      f'{_REQUEST.name} '
                      f'{_REQUEST.patronymic[0]}.')
        _CALLBACK_DATA = f'application_list_show={_REQUEST.id}'
        _keyboard.append([InlineKeyboardButton(text=_TEXT, callback_data=_CALLBACK_DATA)])
    if len(_keyboard) > 10:
        _keyboard.append([InlineKeyboardButton(text='В главное меню', callback_data='main_menu')])
    _REPLY_MARKUP = InlineKeyboardMarkup(_keyboard)

    _TEXT = f'**Всего заявок: {_REQUESTS.count()}**'

    await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='markdown')


async def application_list_show(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _ID: int = update.callback_query.data.split('=')[1]
    _STUDENT = SESSION.query(Student).get(_ID)
    _KEYBOARD = [
        [
            InlineKeyboardButton(text='Назад', callback_data='application_list')
        ],
        [
            InlineKeyboardButton(text='Отклонить', callback_data=f'application_list_reject={_STUDENT.id}'),
            InlineKeyboardButton(text='Принять', callback_data=f'application_list_accept={_STUDENT.id}')
        ]
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _URL: str = str(_STUDENT.url)
    _SURNAME: str = str(_STUDENT.surname)
    _NAME: str = str(_STUDENT.name)
    _PATRONYMIC: str = str(_STUDENT.patronymic)
    _GROUP: str = str(_STUDENT.group)

    _TEXT: str = f'''
<b>ФИО и Группа:</b>
<code>Ф: {_SURNAME}
И: {_NAME}
О: {_PATRONYMIC}
Г: {_GROUP}</code>

<b>Telegram:</b>
ID: <code>{_ID}</code>
Tag: @{_URL}
    '''

    await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')


async def application_list_reject(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _ID: int = update.callback_query.data.split('=')[1]
    _STUDENT = SESSION.query(Student).get(_ID)

    _TEXT: str = f'''
<b>Ваша заявка отклонена:</b>

<code>Ф: {_STUDENT.surname}
И: {_STUDENT.name}
О: {_STUDENT.patronymic}
Г: {_STUDENT.group}</code>
    '''

    _STUDENT.surname = ''
    _STUDENT.name = ''
    _STUDENT.patronymic = ''
    _STUDENT.group = ''
    _STUDENT.valid = 0
    SESSION.commit()

    await _BOT.send_message(chat_id=_ID, text=_TEXT, parse_mode='HTML')
    await application_list(update)


async def application_list_accept(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _ID: int = update.callback_query.data.split('=')[1]
    _STUDENT = SESSION.query(Student).get(_ID)

    _KEYBOARD = [
        [
            InlineKeyboardButton(text='В главное меню', callback_data='student_main')
        ],
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _TEXT: str = f'''
<b>Ваша заявка одобрена:</b>

<code>Ф: {_STUDENT.surname}
И: {_STUDENT.name}
О: {_STUDENT.patronymic}
Г: {_STUDENT.group}</code>
    '''

    _STUDENT.valid = 2
    SESSION.commit()

    await _BOT.send_message(chat_id=_ID, text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')
    await application_list(update)
    await update_bot_name(update)


async def student_main(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _KEYBOARD = [
        [
            InlineKeyboardButton(text='Турнир', callback_data='?')
        ],
        [
            InlineKeyboardButton(text='Участники', callback_data='students_list')
        ]
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _TEXT: str = '<b>Главное меню</b>'

    if update.callback_query:
        await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')
    else:
        await update.message.reply_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')


async def update_bot_name(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _STUDENTS = SESSION.query(Student).filter_by(valid=2)
    _COUNT: int = _STUDENTS.count()
    _NAME: str = f'Осталось мест: {64 - _COUNT}'
    if _COUNT >= 64:
        _NAME = 'Регистрация закрыта'
    await update.get_bot().set_my_name(name=_NAME)


async def students_list(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _STUDENTS = SESSION.query(Student).filter_by(valid=2)
    _KEYBOARD = [
        [InlineKeyboardButton(text='В главное меню', callback_data='student_main')]
    ]

    for _STUDENT in _STUDENTS:
        _TEXT: str = (f'{_STUDENT.group} '
                      f'{_STUDENT.surname} '
                      f'{_STUDENT.name} '
                      f'{_STUDENT.patronymic[0]}.')
        _CALLBACK_DATA: str = f'students_list_show={_STUDENT.id}'
        _KEYBOARD.append([InlineKeyboardButton(text=_TEXT, callback_data=_CALLBACK_DATA)])
    if len(_KEYBOARD) > 10:
        _KEYBOARD.append([InlineKeyboardButton(text='В главное меню', callback_data='student_main')])
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _TEXT: str = '<b>Список студентов:</b>'

    await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')


async def students_list_show(update) -> None:
    """
    view
    :param update:
    :return:
    """
    _ID: int = update.callback_query.data.split('=')[1]
    _STUDENT = SESSION.query(Student).get(_ID)
    _KEYBOARD = [
        [
            InlineKeyboardButton(text='Назад', callback_data='students_list')
        ]
    ]
    _REPLY_MARKUP = InlineKeyboardMarkup(_KEYBOARD)

    _URL: str = str(_STUDENT.url)
    _SURNAME: str = str(_STUDENT.surname)
    _NAME: str = str(_STUDENT.name)
    _PATRONYMIC: str = str(_STUDENT.patronymic)
    _GROUP: str = str(_STUDENT.group)

    _TEXT: str = f'''
<b>ФИО и Группа:</b>
<code>Ф: {_SURNAME}
И: {_NAME}
О: {_PATRONYMIC}
Г: {_GROUP}</code>

<b>Telegram:</b>
ID: <code>{_ID}</code>
Tag: @{_URL}
    '''

    await update.callback_query.edit_message_text(text=_TEXT, reply_markup=_REPLY_MARKUP, parse_mode='HTML')
