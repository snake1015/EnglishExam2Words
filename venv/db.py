# Author Simon
# description: db operate

# -*- encoding=utf-8 -*-

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


db_st = 'sqlite:///words.db'
engine = create_engine(db_st)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
dbcxn = DBSession()

class Words(Base):
    '''
    创建表 words
    '''
    __tablename__ = 'words'
    wordname = Column(String(20), primary_key=True)
    times = Column(Integer, default=0)
    exp = Column(String(50), default='')
    phonogram = Column(String(30), default='')
    is_valid = Column(Integer, default=0)
    rep1 = Column(String(30), default='')  #预留字段
    rep2 = Column(String(30), default='')  # 预留字段


def db_init():
    Base.metadata.create_all(engine)

def db_insert(value):
    if len(value) < 5:
        for i in range[len(value):5]:
            value[int(i)]=''
    new_words = Words(wordname=value[0], times=value[1], exp=value[2], phonogram=value[3],is_valid=value[4])
    dbcxn.add()
    dbcxn.flush()

def db_update(value, tableName):
    if len(value) < 5:
        for i in range[len(value):5]:
            value[int(i)]=''
    up_qurey = dbcxn.query(tableName).filter(tableName.wordname==value[0]).one()
    if not up_qurey.exp or not up_qurey.phonogram:
        up_qurey.exp = value[2]
        up_qurey.phonogram = value[3]
        dbcxn.flush()
    else:
        pass


def db_commit():
    DBSession().commit()

def db_close():
    DBSession().close()





