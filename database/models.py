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

# noinspection PyUnresolvedReferences
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base

_BASE: any = declarative_base()


class Team(_BASE):
    """Team Model

    Model representing a team with the following fields:

    - ``id: Integer``
    - ``url: String``
    - ``name: String``
    - ``leader: JSON``
    - ``members: JSON``
    - ``valid: Integer``

    """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    leader = Column(JSON)
    members = Column(JSON)
    valid = Column(Integer)

    def __repr__(self) -> str:
        return (f'<Team('
                f'id={self.id}, '
                f'url={self.url}, '
                f'name={self.name}, '
                f'leader={self.leader}, '
                f'members={self.members}, '
                f'valid={self.valid}>')

# class Bracket(_BASE):
#     """Bracket Model
#
#     Model representing a bracket with the following fields:
#
#     - ``id: Integer``
#     - ``tour: Integer``
#     - ``student_1: Integer``
#     - ``student_2: Integer``
#     - ``winner: Integer``
#
#     """
#     __tablename__ = 'brackets'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tour = Column(Integer, nullable=False)
#     level = Column(Integer, nullable=False)
#     student_1 = Column(Integer, ForeignKey('students.id'))
#     student_2 = Column(Integer, ForeignKey('students.id'))
#     winner = Column(Integer, ForeignKey('students.id'))
#
#     def __repr__(self):
#         return (f"<Bracket("
#                 f"id={self.id},"
#                 f"tour={self.tour},"
#                 f"level={self.level},"
#                 f"student_1={self.student_1},"
#                 f"student_2={self.student_2},"
#                 f"winner={self.winner})>")
