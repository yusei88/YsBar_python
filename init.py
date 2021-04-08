from sqlalchemy import create_engine, Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ysbar.db',echo=True)

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False)
    pswd = Column(String(256),nullable=False)

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False)
    path = Column(String(100))
    text = Column(String(300))

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    date = Column(DATETIME,nullable=False)
    user_id = Column(Integer,nullable=False)
    menu_id = Column(Integer,nullable=False)

Base.metadata.create_all(bind=engine)#Table作成