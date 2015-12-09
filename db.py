from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref, aliased
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

import os

Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL', 'postgres://localhost/recipehub_service'),
                       convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer(), primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    title = Column(String(140))
    description = Column(String(255))
    user_id = Column(Integer())
    fork_of_id = Column(Integer(), ForeignKey('recipe.id'), nullable=True)
    data_id = Column(Integer(), ForeignKey('recipe_data.id'), nullable=False)
    data = relationship('RecipeData', backref=
        backref('recipes', lazy='joined'))

class RecipeData(Base):
    __tablename__ = 'recipe_data'
    id = Column(Integer(), primary_key=True)
    message = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    ingredients = Column(JSON())
    steps = Column(JSON())
    parent_id = Column(Integer(), ForeignKey('recipe_data.id'))
    children = relationship('RecipeData', backref=
        backref('parent', lazy='joined', remote_side=[id]))
