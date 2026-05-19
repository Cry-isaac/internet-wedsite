import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

#Таблица отзыва
class Review(SqlAlchemyBase):
    #Название таблицы
    __tablename__ = 'reviews'

    #Столбцы
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    stars = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    review = sqlalchemy.Column(sqlalchemy.String)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    hotel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('hotels.id'), nullable=False)


    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    #Отношения
    user = relationship('User', back_populates='reviews')
    hotel = relationship('Hotel', back_populates='reviews')

    def __repr__(self):
        return f'<Review hotel: {self.hotel_id}, user_id: {self.user_id}, stars: {self.stars}, review: {self.review}>'