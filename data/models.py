import sqlalchemy
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

from data.db_session import SqlAlchemyBase

Base = declarative_base()

# Промежуточная таблица User ↔ Reservation
user_reservations = Table(
    'user_reservations',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True),
    sqlalchemy.Column('reservation_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('reservations.id'), primary_key=True)
)

# Промежуточная таблица Hotel ↔ Reservation
hotel_reservations = Table(
    'hotel_reservations',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('hotel_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('hotels.id'), primary_key=True),
    sqlalchemy.Column('reservation_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('reservations.id'), primary_key=True)
)