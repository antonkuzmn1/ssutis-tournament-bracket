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

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from common.parser import parse_snpg
from database.engine import SESSION
from database.models import Team


class UserMethods:
    """

    User methods

    """

    _UPDATE: Update = None
    _CONTEXT: ContextTypes.DEFAULT_TYPE = None

    _ID: int = None
    _URL: str = None
    _TEAM: Team = None

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """

        Constructor for UserMethods class
        :param update:
        :param context:

        """
        # print(json.dumps(update.to_dict(), ensure_ascii=False, indent=4))
        self._UPDATE: Update = update
        self._CONTEXT: ContextTypes.DEFAULT_TYPE = context
        self._ID: int = update.effective_user.id
        self._URL: str = update.effective_user.username
        self._TEAM: Team = self._get_team()

    async def entry(self) -> None:
        """

        Point of entry

        """
        if self._UPDATE.callback_query is not None:
            if self._UPDATE.callback_query.data == 'no_action':
                return
        await self._validation_controller()

    async def _validation_controller(self) -> None:
        """

        Validation controller
        :return:

        """
        match self._TEAM.valid:
            case 0:
                await self._nonvalid_controller()
            case 1:
                print('Validation in process')
            case 2:
                print('Validated. First elimination')
            case 3:
                print('Validated. Second elimination')
            case 4:
                print('Validated. Dropped out')
            case _:
                raise AssertionError("Unexpected validation status")

    async def _nonvalid_controller(self) -> None:
        """

        Non valid controller for case valid == 0
        :return:

        """
        match None:
            case self._TEAM.name:
                await self._team_name()
            case self._TEAM.leader:
                await self._team_leader()
            case _:
                await self._menu_nonvalid_controller()

    async def _team_name(self) -> None:
        """

        match case for method handler
        :return:

        """
        match self._get_type_of_handler():
            case 1:
                await self._send_request_team_name()
            case 2:
                await self._send_request_team_name()
            case 3:
                await self._set_team_name()
            case _:
                raise AssertionError("Unexpected")

    async def _send_request_team_name(self, error: str = None) -> None:
        """

        Send request message for team name
        :param error: error message, if needed
        :return:

        """
        TEXT: str = 'Введите название вашей команды'
        TEXT_FOR_SEND: str = TEXT if error is None else f'Ошибка: {error}\n\n{TEXT}'
        if self._UPDATE.callback_query is None:
            await self._UPDATE.message.reply_text(text=TEXT_FOR_SEND,
                                                  parse_mode=ParseMode.MARKDOWN)
        else:
            await self._UPDATE.callback_query.delete_message()
            await self._CONTEXT.bot.send_message(chat_id=self._ID,
                                                 text=TEXT_FOR_SEND,
                                                 parse_mode=ParseMode.MARKDOWN)

    async def _set_team_name(self) -> None:
        """

        Set team name if all check will be passed

        Redirect to ``_send_request_team_name()`` if checks not passed
        :return:

        """
        NAME: str = self._UPDATE.message.text

        if len(NAME) < 3:
            await self._send_request_team_name(error='Название команды должно содержать не менее 3-х символов')
            return

        self._TEAM.name = NAME
        SESSION.commit()

        await self._send_request_team_leader()

    async def _team_leader(self) -> None:
        """

        match case for method handler
        :return:

        """
        match self._get_type_of_handler():
            case 1:
                print('Not allowed')
            case 2:
                await self._send_request_team_leader()
            case 3:
                await self._set_team_leader()
            case _:
                raise AssertionError("Unexpected")

    async def _send_request_team_leader(self, error: str = None) -> None:
        """

        Send request message for team leader
        :param error: error message, if needed
        :return:

        """
        TEXT: str = ('Введите ваше ФИО, учебную группу и игровой никнейм в следующем формате:\n\n'
                     'Иванов Иван Иванович АА-111\n'
                     'Ivanov1337')
        TEXT_FOR_SEND: str = TEXT if error is None else f'Ошибка: {error}\n\n{TEXT}'
        await self._UPDATE.message.reply_text(text=TEXT_FOR_SEND,
                                              parse_mode=ParseMode.MARKDOWN)

    async def _set_team_leader(self) -> None:
        """

        Set team leader if all check will be passed

        Redirect to ``_send_request_team_leader()`` if checks not passed
        :return:

        """
        INPUT: str = self._UPDATE.message.text
        DATA = parse_snpg(value=INPUT)

        if not DATA:
            await self._send_request_team_leader(error='Некорректный формат')
            return

        self._TEAM.leader = DATA
        SESSION.commit()

        await self._send_menu_nonvalid()

    async def _menu_nonvalid_controller(self) -> None:
        """

        Main menu for nonvalid users
        :return:

        """
        match self._get_type_of_handler():
            case 1:
                await self._menu_nonvalid_callback_controller()
            case 2:
                await self._send_menu_nonvalid()
            case 3:
                return
            case _:
                raise AssertionError("Unexpected")

    async def _menu_nonvalid_callback_controller(self) -> None:
        """

        Callback controller for nonvalid users
        :return:

        """
        match self._UPDATE.callback_query.data:
            case 'nonvalid_refil':
                await self._menu_nonvalid_refil()
            case 'nonvalid_addmember':
                print('not working')
            case 'nonvalid_submit':
                print('not working')
            case _:
                raise AssertionError("Unexpected")

    async def _menu_nonvalid_refil(self) -> None:
        """

        Drop teamname and leader data
        :return:

        """
        self._TEAM.leader = None
        self._TEAM.name = None
        SESSION.commit()
        await self._send_request_team_name()

    async def _send_menu_nonvalid(self) -> None:
        """

        Send menu-message for nonvalid users
        :return:

        """
        KEYBOARD: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text='Заполнить заново', callback_data='nonvalid_refil')],
            [InlineKeyboardButton(text='Добавить участника', callback_data='nonvalid_addmember')],
            [InlineKeyboardButton(text='Отправить заявку', callback_data='nonvalid_submit')]
        ]
        REPLY_MARKUP: InlineKeyboardMarkup = InlineKeyboardMarkup(KEYBOARD)

        TEXT: str = (f'''
<b>Главное меню</b>

Команда: <code>{self._TEAM.name}</code>

Лидер:
<code>Ф</code>: <code>{self._TEAM.leader['surname']}</code>
<code>И</code>: <code>{self._TEAM.leader['name']}</code>
<code>О</code>: <code>{self._TEAM.leader['patronymic']}</code>
<code>Г</code>: <code>{self._TEAM.leader['group']}</code>
<code>Н</code>: <code>{self._TEAM.leader['nickname']}</code>
        ''')

        await self._UPDATE.message.reply_text(text=TEXT,
                                              parse_mode=ParseMode.HTML,
                                              reply_markup=REPLY_MARKUP)

    def _get_team(self) -> Team:
        """

        Get a team entity if exists, or create a new one if not exists
        :return Team:

        """
        TEAM: Team = SESSION.query(Team).get(self._ID)

        if TEAM is None:
            NEW_TEAM: Team = Team(id=self._ID,
                                  url=self._URL,
                                  name=None,
                                  leader=None,
                                  members=None,
                                  valid=0)
            SESSION.add(NEW_TEAM)
            SESSION.commit()
            return NEW_TEAM

        TEAM.url = self._URL
        SESSION.commit()
        return TEAM

    def _get_type_of_handler(self) -> int:
        """

        Get a type of handler

        1 - callback_query

        2 - /start

        3 - message

        """
        if self._UPDATE.callback_query is not None:
            return 1
        elif self._UPDATE.message.text == '/start':
            return 2
        else:
            return 3
