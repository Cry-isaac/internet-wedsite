import sqlalchemy
from sqlalchemy.orm import relationship

from .models import user_reservations, hotel_reservations
from .db_session import SqlAlchemyBase

#Таблица дат бронирования
class BookedDate(SqlAlchemyBase):
    __tablename__ = 'reservations'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pet_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    check_in = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    check_out = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    total_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    hotel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hotels.id"), nullable=False)

    user = relationship('User', back_populates='reservations')
    hotel = relationship('Hotel', back_populates='reservations')


    def __repr__(self):
        return f'<Reservation hotel: {self.hotel_id}, user_id: {self.user_id}, date: {self.date}>'