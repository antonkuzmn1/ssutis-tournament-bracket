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
# from typing import List
#
# from sqlalchemy import or_
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.constants import ParseMode
# from telegram.ext import CallbackContext
#
# from bot.tools.bridge import get_student, get_level
# from config import TELEGRAM_ADMIN
# from database.bundle import generate_bracket
# from database.engine import SESSION
# from database.models import Bracket, Student
#
# _STUDENT_MAIN_BUTTON: List[InlineKeyboardButton] = [
#     InlineKeyboardButton(text='В главное меню', callback_data='student_main')
# ]
#
#
# async def _get_opponent_id(your_id: int) -> int:
#     """
#
#     Get the opponent's id by bracket cell
#     :param your_id:
#     :return:
#
#     """
#     BRACKET_ROW = (SESSION.query(Bracket)
#                    .filter(or_(Bracket.student_1 == your_id,
#                                Bracket.student_2 == your_id)).first())
#     BRACKET_CELL_OPPONENT: int = 1 if BRACKET_ROW.student_2 == your_id else 2
#     OPPONENT_ID: int = BRACKET_ROW.student_1 if BRACKET_CELL_OPPONENT == 1 else BRACKET_ROW.student_2
#     return int(OPPONENT_ID)
#
#
# async def _get_available_grid_cells(update: Update) -> None:
#     """
#
#     if the tournament grid cell is NOT YET selected
#
#     :param update:
#     :return:
#
#     """
#     STUDENT = await get_student(update)
#     LEVEL: int = get_level(STUDENT)
#
#     BRACKET = SESSION.query(Bracket).filter_by(level=LEVEL).all()
#
#     KEYBOARD: List[List[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#
#     for ROW in BRACKET:
#         STUDENT_1_ID = ROW.student_1
#         STUDENT_1 = None if STUDENT_1_ID is None else SESSION.query(Student).get(STUDENT_1_ID)
#         STUDENT_1_NAME = f'[{ROW.id}-1] Свободно' \
#             if STUDENT_1 is None else (f'[{ROW.id}-1] '
#                                        f'{STUDENT_1.group} '
#                                        f'{STUDENT_1.surname} '
#                                        f'{list(STUDENT_1.name)[0]}. '
#                                        f'{list(STUDENT_1.patronymic)[0]}.')
#         CALLBACK_DATA_1 = f'tb_engine=set=1={ROW.id}' if STUDENT_1 is None else 'no_action'
#
#         STUDENT_2_ID = ROW.student_2
#         STUDENT_2 = None if STUDENT_2_ID is None else SESSION.query(Student).get(STUDENT_2_ID)
#         STUDENT_2_NAME = f'[{ROW.id}-2] Свободно' \
#             if STUDENT_2 is None else (f'[{ROW.id}-2] '
#                                        f'{STUDENT_2.group} '
#                                        f'{STUDENT_2.surname} '
#                                        f'{list(STUDENT_2.name)[0]}. '
#                                        f'{list(STUDENT_2.patronymic)[0]}.')
#         CALLBACK_DATA_2 = f'tb_engine=set=2={ROW.id}' if STUDENT_2 is None else 'no_action'
#
#         KEYBOARD.append([InlineKeyboardButton(text=STUDENT_1_NAME, callback_data=CALLBACK_DATA_1),
#                          InlineKeyboardButton(text=STUDENT_2_NAME, callback_data=CALLBACK_DATA_2)])
#
#     KEYBOARD.append(_STUDENT_MAIN_BUTTON)
#     REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#
#     TEXT = f'Уровень: {LEVEL}\nВыберите место'
#
#     await update.callback_query.edit_message_text(text=TEXT, reply_markup=REPLY_MARKUP)
#
#
# async def _get_grid_cell_data(update: Update):
#     """
#
#     if a tournament grid cell is ALREADY selected
#
#     :param update:
#     :return:
#
#     """
#     ID: int = update.callback_query.message.chat.id
#     STUDENT = await get_student(update)
#     LEVEL: int = get_level(STUDENT)
#     ROW_CURRENT = (SESSION.query(Bracket)
#                    .filter_by(level=LEVEL)
#                    .filter(or_(Bracket.student_1 == STUDENT.id,
#                                Bracket.student_2 == STUDENT.id)).first())
#
#     CELL_NUMBER = 1 if ROW_CURRENT.student_1 == ID else 2
#
#     STUDENT_OPPONENT = SESSION.query(Student).get(
#         ROW_CURRENT.student_2 if CELL_NUMBER == 1 else ROW_CURRENT.student_1
#     )
#
#     KEYBOARD: List[List[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#     if STUDENT_OPPONENT is not None:
#         KEYBOARD.append([InlineKeyboardButton(text='Я победил', callback_data='tb_engine=win_request')])
#     REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#
#     OPPONENT = 'Ожидание оппонента...' \
#         if STUDENT_OPPONENT is None else (f'{STUDENT_OPPONENT.group} '
#                                           f'{STUDENT_OPPONENT.surname} '
#                                           f'{STUDENT_OPPONENT.name} '
#                                           f'{STUDENT_OPPONENT.patronymic}\n'
#                                           f'@{STUDENT_OPPONENT.url}')
#
#     TEXT = f'Оппонент:\n{OPPONENT}\n\nНомер ячейки: {ROW_CURRENT.id}'
#
#     await update.callback_query.edit_message_text(text=TEXT,
#                                                   reply_markup=REPLY_MARKUP,
#                                                   parse_mode=ParseMode.HTML)
#
#
# async def tb_engine(update: Update, context: CallbackContext) -> None:
#     """
#
#     Tournament bracket's engine
#     :param context:
#     :param update:
#     :return:
#
#     """
#     await generate_bracket()
#
#     if update.callback_query is not None:
#         UNVERIFIED_DATA: list[str] = update.callback_query.data.split('=')
#         ID: int = update.callback_query.message.chat.id
#
#         STUDENT: Student = await get_student(update)
#         LEVEL: int = get_level(STUDENT)
#
#         # BRACKET = SESSION.query(Bracket).filter_by(level=LEVEL).all()
#         ROW_CURRENT: Bracket = (SESSION.query(Bracket)
#                                 .filter_by(level=LEVEL, winner=None)
#                                 .filter(or_(Bracket.student_1 == STUDENT.id,
#                                             Bracket.student_2 == STUDENT.id)).first())
#
#         if ID == TELEGRAM_ADMIN:
#             # admin's logic is here
#             KEYBOARD: List[List[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#             REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#             # canvas module required:
#             TEXT: str = 'Визуализация турнирной сетки\nОшибка: модуль для визуализации еще не готов'
#             await update.callback_query.edit_message_text(text=TEXT, reply_markup=REPLY_MARKUP)
#
#         else:
#             # user's logic is here
#             if len(UNVERIFIED_DATA) == 1:
#                 # type get
#                 if ROW_CURRENT is None:
#                     await _get_available_grid_cells(update=update)
#                 else:
#                     await _get_grid_cell_data(update=update)
#
#             else:
#                 # type update
#                 match UNVERIFIED_DATA[1]:
#                     case 'set':
#                         # cell selection
#                         ROW_STUDENT = int(UNVERIFIED_DATA[2])
#                         ROW_ID = int(UNVERIFIED_DATA[3])
#                         ROW = SESSION.query(Bracket).get(ROW_ID)
#
#                         match ROW_STUDENT:
#                             case 1:
#                                 if ROW.student_1 is None:
#                                     ROW.student_1 = ID
#                                     SESSION.commit()
#
#                                     KEYBOARD: List[List[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#                                     REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#
#                                     STUDENT_2 = SESSION.query(Student).get(ROW.student_2)
#
#                                     OPPONENT = 'Ожидание оппонента...' \
#                                         if STUDENT_2 is None else (f'{STUDENT_2.group} '
#                                                                    f'{STUDENT_2.surname} '
#                                                                    f'{list(STUDENT_2.name)[0]}. '
#                                                                    f'{list(STUDENT_2.patronymic)[0]}.\n'
#                                                                    f'@{STUDENT_2.url}')
#
#                                     TEXT = f'Оппонент:\n{OPPONENT}\n\nНомер ячейки: {ROW_ID}'
#
#                                     await update.callback_query.edit_message_text(text=TEXT,
#                                                                                   reply_markup=REPLY_MARKUP,
#                                                                                   parse_mode=ParseMode.HTML)
#                                     if STUDENT_2 is not None:
#                                         await context.bot.send_message(chat_id=STUDENT_2.id, text='Оппонент найден')
#                             case 2:
#                                 if ROW.student_2 is None:
#                                     ROW.student_2 = ID
#                                     SESSION.commit()
#
#                                     KEYBOARD: List[List[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#                                     REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#
#                                     STUDENT_1 = SESSION.query(Student).get(ROW.student_1)
#
#                                     OPPONENT = 'Ожидание оппонента...' \
#                                         if STUDENT_1 is None else (f'{STUDENT_1.group} '
#                                                                    f'{STUDENT_1.surname} '
#                                                                    f'{list(STUDENT_1.name)[0]}. '
#                                                                    f'{list(STUDENT_1.patronymic)[0]}.\n'
#                                                                    f'@{STUDENT_1.url}')
#
#                                     TEXT = f'Оппонент:\n{OPPONENT}\n\nНомер ячейки: {ROW_ID}'
#
#                                     await update.callback_query.edit_message_text(text=TEXT,
#                                                                                   reply_markup=REPLY_MARKUP,
#                                                                                   parse_mode=ParseMode.HTML)
#                                     if STUDENT_1 is not None:
#                                         await context.bot.send_message(chat_id=STUDENT_1.id, text='Оппонент найден')
#                             case _:
#                                 assert ('RECIEVED UNDEFINED DATA: {}'.format(UNVERIFIED_DATA[2]))
#
#                     case 'win_request':
#                         # send win-request
#                         OPPONENT_ID: int = await _get_opponent_id(your_id=ID)
#
#                         KEYBOARD = [[
#                             InlineKeyboardButton(text='Да, я проиграл', callback_data='tb_engine=win_confirm'),
#                             InlineKeyboardButton(text='Нет, это ошибка', callback_data='tb_engine=win_decline')
#                         ]]
#                         REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)
#
#                         TEXT = ('Оппонет заявляет о своей победе - это правда?'
#                                 '\nНажмите \'Да, я проиграл\', '
#                                 'если вы подтверждаете победу вашего оппонента и ваше поражение'
#                                 '\nНажмите \'Нет, это ошибка\', '
#                                 'если вы не согласны с заявлением вашего оппонента и считаете его ошибочным')
#
#                         await context.bot.send_message(chat_id=OPPONENT_ID, text=TEXT, reply_markup=REPLY_MARKUP)
#                         await context.bot.send_message(chat_id=ID, text='Предложение отправлено оппоненту')
#
#                     case 'win_confirm':
#                         # confirm win-request
#                         OPPONENT_ID: int = await _get_opponent_id(your_id=ID)
#                         ROW_CURRENT.winner = ID
#                         SESSION.commit()
#
#                         KEYBOARD: list[list[InlineKeyboardButton]] = [_STUDENT_MAIN_BUTTON]
#                         REPLAY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)
#
#                         TEXT_1: str = 'Ваша победа зачтена, вернитесь в главное меню для обновления турнирного окна'
#                         await context.bot.send_message(chat_id=OPPONENT_ID, text=TEXT_1, reply_markup=REPLAY_MARKUP)
#
#                         TEXT_2: str = 'Ваша неудача зачтена, вернитесь в главное меню для обновления турнирного окна'
#                         await update.callback_query.edit_message_text(text=TEXT_2, reply_markup=REPLAY_MARKUP)
#
#                     case 'win_decline':
#                         # decline win-request
#                         OPPONENT_ID: int = await _get_opponent_id(your_id=ID)
#
#                         TEXT = 'Оппонент счел ваше заявление о победе ошибочным'
#
#                         await context.bot.send_message(chat_id=OPPONENT_ID, text=TEXT)
#                         await context.bot.delete_message(chat_id=ID,
#                                                          message_id=update.callback_query.message.message_id)
#
#                     case _:
#                         assert ('RECIEVED UNDEFINED DATA: {}'.format(UNVERIFIED_DATA[1]))
