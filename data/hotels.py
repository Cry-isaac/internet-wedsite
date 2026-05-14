import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

#Таблица отеля
class Hotel(SqlAlchemyBase):
    #Название таблицы
    __tablename__ = 'hotels'

    #Столбцы
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String)
    stars = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'))
    reservations_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('reservations.id'), nullable=True)

    #Отношения
    user = relationship('User', back_populates='hotel')
    review = relationship('Review', back_populates='hotel')
    # booked_date = orm.relationship('BookedDate', secondary=association_table_hotel, back_populates='hotels')

    def __repr__(self):
        return f'<Hotel title: {self.title}, stars: {self.stars}, location: {self.location}, user_id: {self.user_id}>'
