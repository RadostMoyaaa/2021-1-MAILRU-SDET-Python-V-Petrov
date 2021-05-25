from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUsers(Base):  # Модель пользователи
    __tablename__ = 'test_users'

    def __repr__(self):
        return f"<test_users(" \
               f"id='{self.id}'," \
               f"username='{self.username}', " \
               f"password='{self.password}', " \
               f"email='{self.email}', " \
               f"access='{self.access}', " \
               f"active='{self.active}', " \
               f"start_active_time='{self.start_active_time}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(16), default=None, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger, default=None)
    active = Column(SmallInteger, default=None)
    start_active_time = Column(DateTime, default=None)
