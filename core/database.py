from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Здесь осуществляется подключение к БД и создаются сессии SQLAlchemy

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///db.sqlite')

SessionLocal = sessionmaker(bind=engine)
