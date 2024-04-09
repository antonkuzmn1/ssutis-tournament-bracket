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

from database.engine import SESSION
from database.models import Student


def get_student(update):
    """
    Get student from database and insert new student into the database if it doesn't exist.
    :param update: Update handler by Telegram API
    :return: ``Student`` -- Student alchemy model
    """
    _ID: int = update.effective_user.id
    _URL: str = update.effective_user.username

    student = SESSION.query(Student).get(_ID)
    if student is None:
        _NEW_STUDENT = Student(id=_ID,
                               url=_URL,
                               surname='',
                               name='',
                               patronymic='',
                               group='',
                               location='main',
                               valid=0)
        SESSION.add(_NEW_STUDENT)
        SESSION.commit()
        return SESSION.query(Student).get(_ID)
    student.url = _URL
    SESSION.commit()
    return student
