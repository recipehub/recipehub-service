from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import JSON

import os

Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL', 'postgres://localhost/recipehub_service'),
                       convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))

class Recipie(Base):
    __tablename__ = 'recipie'
    id = Column(Integer(), primary_key=True)
    title = Column(String(140))
    user_id = Column(Integer())
    fork_of_id = Column(Integer(), ForeignKey('recipie.id'), nullable=True)
    data_id = Column(Integer(), ForeignKey('recipie_data.id'), nullable=False)
    data = relationship('RecipieData', backref=
        backref('recipies', lazy='joined'))

class RecipieData(Base):
    __tablename__ = 'recipie_data'
    id = Column(Integer(), primary_key=True)
    ingredients = Column(JSON())
    steps = Column(JSON())
    parent_id = Column(Integer(), ForeignKey('recipie_data.id'))
    children = relationship('RecipieData', backref=
        backref('parent', lazy='joined', remote_side=[id]))
