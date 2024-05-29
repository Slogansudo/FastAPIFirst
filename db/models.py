from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from db.database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    travel_category = relationship('TravelCategory', back_populates='author')
    comments = relationship('Comments', back_populates='users')

    def __repr__(self):
        return self.email


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    places = relationship('Places', back_populates='address')

    def __repr__(self):
        return self.name


class Places(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    address = relationship('Address', back_populates='places')
    travels = relationship('Travels', back_populates='places')

    def __repr__(self):
        return self.name


class TravelCategory(Base):
    __tablename__ = 'travel_category'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(50), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)
    author = relationship('Users', back_populates='travel_category')
    travels = relationship('Travels', back_populates='travel_category')

    def __repr__(self):
        return self.name


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)
    users = relationship('Users', back_populates='comments')
    travels = relationship('Travels', back_populates='comments')

    def __repr__(self):
        return self.text


class Travels(Base):
    __tablename__ = 'travels'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float)
    price_type = Column(String(10), default='$')
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('travel_category.id'))
    palaces_id = Column(Integer, ForeignKey('places.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    discounts = Column(Float, default=0)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    comments = relationship('Comments', back_populates='travels')
    places = relationship('Places', back_populates='travels')
    travel_category = relationship('TravelCategory', back_populates='travels')

    def __repr__(self):
        return self.name
