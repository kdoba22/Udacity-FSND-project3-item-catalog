from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
import sqlalchemy.sql.functions as func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
#    password = Column(String(100), nullable=True)

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    items = relationship("Item", cascade="delete")

    def __str__(self):
        return self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    last_update = Column(
        DateTime, server_default=func.now(),
        onupdate=func.now())

    @validates('description')
    def validate_description(self, key, description):
        if description == '':
            raise ValueError(
                "please populate description")
        return description

    @property
    def serialize(self):
        return {
            'cat_id': self.category_id,
            'description': self.description,
            'id': self.id,
            'name': self.name,
        }

engine = create_engine('sqlite:///catalogmenu.db')

Base.metadata.create_all(engine)
