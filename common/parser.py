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

import re
from config import DEBUG


def _parse_name(value):
    """
    patternt
    :param value:
    :return:
    """
    return re.match(r'[а-яА-Я]{2,30}', value, re.IGNORECASE).group().title()


def _parse_group(value):
    """
    pattern
    :param value:
    :return:
    """
    _WITH_DASH = re.match(r'[а-яА-Я]{1,4}-\d{1,4}', value, re.IGNORECASE)
    _WITHOUT_DASH = re.match(r'([а-яА-Я]{1,4})(\d{1,4})', value, re.IGNORECASE)

    if _WITH_DASH:
        return _WITH_DASH.group().upper()

    if _WITHOUT_DASH:
        _CHARS = _WITHOUT_DASH.group(1).upper()
        _DIGITS = _WITHOUT_DASH.group(2)
        return f'{_CHARS}-{_DIGITS}'


def parse_snpg(value):
    """
    Example N1:
        - input -- иванов ИВан иваНОВИЧ аа111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"Иванович","group": "АА-111"}

    Example N2
        - input -- иванов ИВан аа-111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"-","group": "АА-111"}
    """
    result = dict(
        surname="",
        name="",
        patronymic="",
        group=""
    )

    if DEBUG:
        print('text:', value)

    _WORDS = value.split(' ')
    if DEBUG:
        print('len:', len(_WORDS))
        print('words:', _WORDS)

    if len(_WORDS) not in [3, 4]:
        return result

    _SURNAME: str = _parse_name(_WORDS[0])
    if DEBUG:
        print('S:', _SURNAME)

    _NAME: str = _parse_name(_WORDS[1])
    if DEBUG:
        print('N:', _NAME)

    _PATRONYMIC: str = _parse_name(_WORDS[2]) if len(_WORDS) == 4 else '-'
    if DEBUG:
        print('P:', _PATRONYMIC)

    _RAW_GROUP: str = _WORDS[3] if len(_WORDS) == 4 else _WORDS[2]
    _PARSED_GROUP: str = _parse_group(_RAW_GROUP)
    if DEBUG:
        print('G:', _PARSED_GROUP)

    if all([_SURNAME, _NAME, _PATRONYMIC, _PARSED_GROUP != '']):
        if all([_SURNAME, _NAME, _PATRONYMIC, _PARSED_GROUP is not None]):
            result['surname'] = _SURNAME
            result['name'] = _NAME
            result['patronymic'] = _PATRONYMIC
            result['group'] = _PARSED_GROUP

    return result


if __name__ == '__main__':
    """local test"""
    _PREPARED = [
        'Кузьмин анТОН денисович им-271',
        'Кузьмин Антон денисович им271',
        'Кузьмин Антон им271',
        'кузьмин антон денисович',
        ''
    ]

    for i, prepared_text in enumerate(_PREPARED):
        _TEXT: str = input('\n\n\nEnter SNPG: ')
        _SELECTED_TEXT: str = _TEXT if _TEXT != '' else prepared_text
        print(parse_snpg(_SELECTED_TEXT))
