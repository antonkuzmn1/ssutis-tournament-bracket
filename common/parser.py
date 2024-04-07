import re
from config import DEBUG


def parse_name(value):
    return re.match(r'[а-яА-Я]{2,30}', value, re.IGNORECASE).group().title()


def parse_group(value):
    with_dash = re.match(r'[а-яА-Я]{1,4}-\d{1,4}', value, re.IGNORECASE)
    without_dash = re.match(r'([а-яА-Я]{1,4})(\d{1,4})', value, re.IGNORECASE)
    if with_dash:
        return with_dash.group().upper()
    if without_dash:
        chars = without_dash.group(1).upper()
        digits = without_dash.group(2)
        return f'{chars}-{digits}'


def parse_snpg(value):
    """
    Example N1:
        - input -- иванов ИВан иваНОВИЧ аа111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"Иванович","group": "АА-111"}

    Example N2
        - input -- иванов ИВан аа-111
        - return -- {"surname":"Иванов","name":"Иван","patronymic":"-","group": "АА-111"}
    """
    result = {
        "surname": "",
        "name": "",
        "patronymic": "",
        "group": ""
    }

    try:
        if DEBUG:
            print('text:', value)

        words = value.split(' ')
        if DEBUG:
            print('len:', len(words))
            print('words:', words)

        assert (len(words) == 3 or len(words) == 4)

        surname = parse_name(words[0])
        if DEBUG:
            print('S:', surname)

        name = parse_name(words[1])
        if DEBUG:
            print('N:', name)

        patronymic = parse_name(words[2]) if len(words) == 4 else '-'
        if DEBUG:
            print('P:', patronymic)

        raw_group = words[3] if len(words) == 4 else words[2]
        group = parse_group(raw_group)
        if DEBUG:
            print('G:', group)

        if surname != '' and name != '' and patronymic != '' and group != '' and group is not None:
            result['surname'] = surname
            result['name'] = name
            result['patronymic'] = patronymic
            result['group'] = group

        return result
    finally:
        return result


if __name__ == '__main__':
    i = 0
    while True:
        prepared = [
            'Кузьмин анТОН денисович им-271',
            'Кузьмин Антон денисович им271',
            'Кузьмин Антон им271',
        ]
        text = input('\n\n\nEnter SNPG: ')
        for_parse = text if text != '' else prepared[i]
        print(parse_snpg(for_parse))
        i += 1
