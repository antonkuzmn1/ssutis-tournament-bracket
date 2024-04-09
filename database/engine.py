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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_FILE, SQLALCHEMY_DATABASE_URI
from database.models import Base

engine = create_engine(f'{SQLALCHEMY_DATABASE_URI}///{DATABASE_FILE}')

Session = sessionmaker(bind=engine)
SESSION = Session()

Base.metadata.create_all(engine)
