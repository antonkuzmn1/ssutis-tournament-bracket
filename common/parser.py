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


# from config import DEBUG


def _parse_name(value) -> str:
    """
    patternt
    :param value:
    :return:
    """
    return re.match(r'[а-яА-Я-]{2,30}', value, re.IGNORECASE).group().title()


def _parse_group(value) -> str:
    """
    pattern
    :param value:
    :return:
    """
    WITH_DASH = re.match(r'[а-яА-Я]{1,4}-\d{1,4}', value, re.IGNORECASE)
    WITHOUT_DASH = re.match(r'([а-яА-Я]{1,4})(\d{1,4})', value, re.IGNORECASE)

    if WITH_DASH:
        return WITH_DASH.group().upper()

    if WITHOUT_DASH:
        CHARS = WITHOUT_DASH.group(1).upper()
        DIGITS = WITHOUT_DASH.group(2)
        return f'{CHARS}-{DIGITS}'


def parse_snpg(value) -> dict[str, str] | bool:
    """
    Example N1:
        - input -- иванов ИВан иваНОВИЧ аа111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"Иванович","group": "АА-111"}

    Example N2
        - input -- иванов ИВан аа-111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"-","group": "АА-111"}
    """
    try:
        result = dict(
            surname="",
            name="",
            patronymic="",
            group="",
            nickname=""
        )

        DEBUG = True

        if DEBUG:
            print('text:', value)

        SEPARATED_NICKNAME = value.split('\n')
        if DEBUG:
            print(SEPARATED_NICKNAME)
            print('nick:', SEPARATED_NICKNAME[1])

        WORDS = SEPARATED_NICKNAME[0].split(' ')
        if DEBUG:
            print('len:', len(WORDS))
            print('words:', WORDS)

        if len(WORDS) not in [3, 4]:
            return result

        SURNAME: str = _parse_name(WORDS[0])
        if DEBUG:
            print('S:', SURNAME)

        NAME: str = _parse_name(WORDS[1])
        if DEBUG:
            print('N:', NAME)

        PATRONYMIC: str = _parse_name(WORDS[2]) if len(WORDS) == 4 else '-'
        if DEBUG:
            print('P:', PATRONYMIC)

        RAW_GROUP: str = WORDS[3] if len(WORDS) == 4 else WORDS[2]
        PARSED_GROUP: str = _parse_group(RAW_GROUP)
        if DEBUG:
            print('G:', PARSED_GROUP)

        if all([SURNAME, NAME, PATRONYMIC, PARSED_GROUP != '']):
            if all([SURNAME, NAME, PATRONYMIC, PARSED_GROUP is not None]):
                result['surname'] = SURNAME
                result['name'] = NAME
                result['patronymic'] = PATRONYMIC
                result['group'] = PARSED_GROUP
                result['nickname'] = SEPARATED_NICKNAME[1]
                print(result)
                return result
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    """local test"""
    _PREPARED = [
        'Кузьмин анТОН денисович им-271\nAnton13yo',
        'Кузьмин Антон денисович им271\nAnton13yo',
        'Кузьмин Антон им271\nAnton13yo',
        'кузьмин антон денисович\nAnton13yo',
        ''
    ]

    for i, prepared_text in enumerate(_PREPARED):
        _TEXT: str = input('\n\n\nEnter SNPG: ')
        _SELECTED_TEXT: str = _TEXT if _TEXT != '' else prepared_text
        print(parse_snpg(_SELECTED_TEXT))
