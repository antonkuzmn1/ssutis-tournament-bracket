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

# from database.engine import SESSION
# from database.models import Bracket
#
#
# async def generate_bracket() -> None:
#     """
#
#     Generates a random Bracket object and stores it in the database
#     :return:
#
#     """
#     _LEVELS_64 = [(0, 32), (1, 16), (2, 8), (3, 4), (4, 2), (5, 1)]
#
#     if len(SESSION.query(Bracket).all()) == 0:
#
#         for _LEVEL, _COUNT in _LEVELS_64:
#             for _ in range(_COUNT):
#                 _BRACKET = Bracket(tour=1, level=_LEVEL, student_1=None, student_2=None, winner=None)
#                 SESSION.add(_BRACKET)
#
#         SESSION.commit()
