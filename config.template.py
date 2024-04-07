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

# Configuration settings for the application
# Конфигурационные настройки приложения


# Replace this with a telegram bot token
# Замени это реальным токеном действуюшего Telegram бота
TELEGRAM_TOKEN = 'SECRET'
"""
English:
    Token for accessing the Telegram Bot API.

Русский:
    Токен для доступа к Telegram Bot API.
"""

# Replace this with real telegram chat id for administration
# Замени это реальным идентификатором чата Telegram для администрации
TELEGRAM_ADMIN = -1234567890123
"""
English:
    Telegram chat ID for administration.
        Important:
            The ID can go beyond the 32-bit value.
            
            It is strongly recommended to use a 64-bit data type.
            
Русский:
    Идентификатор чата Telegram для администрирования.
        Важно:
            Идентификатор может выходить за пределы 32-битного значения.
            
            Настоятельно рекомендуется использовать 64-битный тип данных.
"""

# By default: database.db
DATABASE_FILE = 'database.db'
"""
English:
    File name of the database used by the application.

Русский:
    Имя файла базы данных, используемой приложением.
"""

# By default: False
DEBUG = False
"""
English:
    Debug mode flag.
    
    Set to True to enable debug mode,
    which may provide more detailed logging
    and error messages for development purposes.

Русский:
    Флаг режима отладки.
    
    Установите значение True, чтобы включить режим отладки,
    который может обеспечить более подробное ведение журнала
    и сообщения об ошибках для целей разработки.
"""
