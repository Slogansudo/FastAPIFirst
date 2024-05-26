from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from databse import Base


class User(Base):
    __table_name__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(String(25), nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return self.email


class Address(Base):
    __table_name__ = 'address'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    def __repr__(self):
        return self.name


class Places(Base):
    __table_name__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(Integer, ForeignKey('address.id'), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    def __repr__(self):
        return self.name


class TravelCategory(Base):
    __table_name__ = 'travel_category'

    id = Column(Integer, primary_key=True)
    author = relationship('User', back_populates='users')
    name = Column(String(50), nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    def __repr__(self):
        return self.name


class Comments(Base):
    __table_name__ = 'comments'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    def __repr__(self):
        return self.text


class Travels(Base):
    __table_name__ = 'travels'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float)
    price_type = Column(String(10), default='$')
    description = Column(Text)
    category = Column(Integer, ForeignKey('travel_category.id'))
    comments = relationship('Comment', back_populates='comments')
    places = relationship('Places', back_populates='places')
    discounts = Column(Float, default=0)
    created_date = Column(DateTime, autoincrement=True)
    updated_date = Column(DateTime, autoincrement=True)

    def __repr__(self):
        return self.name
