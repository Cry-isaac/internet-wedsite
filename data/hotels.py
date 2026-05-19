import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin

from .models import hotel_reservations
from .db_session import SqlAlchemyBase

#Таблица отеля
class Hotel(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'hotels'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    stars = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)  # Владелец отеля

    # Связи
    owner = relationship('User', back_populates='hotels')  # Связь с владельцем
    reservations = relationship('BookedDate', back_populates='hotel', cascade='all, delete-orphan')  # Бронирования отеля
    reviews = relationship('Review', back_populates='hotel')

    def __repr__(self):
        return f'<Hotel title: {self.title}, stars: {self.stars}, location: {self.location}, user_id: {self.user_id}>'

    @validates('stars')
    def validate_stars(self, key, value):
        if value < 1 or value > 5:
            raise ValueError('Количество звёзд должно быть от 1 до 5')
        return value