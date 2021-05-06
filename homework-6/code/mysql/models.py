from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CountRequests(Base):  # Модель общее количество запросов
    __tablename__ = 'count_requests'

    def __repr__(self):
        return f"<CountRequests(" \
               f"id='{self.id}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class CountTyped(Base):  # Модель количество запросов по типу
    __tablename__ = 'count_typed'

    def __repr__(self):
        return f"<count_typed(" \
               f"id='{self.id}'," \
               f"type='{self.name}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    count = Column(Integer, nullable=False)


class BiggestRequestsError(Base):  # Модель самые большие запросы с ошибкой
    __tablename__ = 'biggest_error'

    def __repr__(self):
        return f"<BiggestRequestsError(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"code='{self.code}', " \
               f"size='{self.size}', " \
               f"ip='{self.ip}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    code = Column(String(4), nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)
