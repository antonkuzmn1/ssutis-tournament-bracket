from .db.database import create_connection


def get_db():
    db = create_connection()
    try:
        yield db
    finally:
        db.close()
