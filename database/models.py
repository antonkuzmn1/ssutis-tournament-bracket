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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    """
    **Student Model**

    Model representing a student with the following fields:

    - ``id: Integer``
    - ``url: String``
    - ``surname: String``
    - ``name: String``
    - ``patronymic: String``
    - ``group: String``
    - ``valid: Integer``
    - ``location: String``
    """
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    group = Column(String)
    valid = Column(Integer)
    location = Column(String)


class Bracket(Base):
    """
    **Bracket Model**

    Model representing a bracket with the following fields:

    - ``id: Integer``
    - ``tour: Integer``
    - ``student_1: Integer``
    - ``student_2: Integer``
    - ``winner: Integer``
    """
    __tablename__ = 'brackets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tour = Column(Integer, nullable=False)
    student_1 = Column(Integer, ForeignKey('students.id'))
    student_2 = Column(Integer, ForeignKey('students.id'))
    winner = Column(Integer, ForeignKey('students.id'))
