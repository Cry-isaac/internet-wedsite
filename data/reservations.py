import sqlalchemy
from .db_session import SqlAlchemyBase

#Таблица дат бронирования
class BookedDate(SqlAlchemyBase):
    #Название таблицы
    __tablename__ = 'reservations'

    #Столбцы
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    hotel_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("hotels.id"), nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), nullable=False)

    check_in = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    check_out = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    total_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    #Отношения
    # user = orm.relationship('User', secondary=association_table_user, back_populates='booked_date')
    # hotels = orm.relationship('Hotel', secondary=association_table_hotel, back_populates='booked_date')

    def __repr__(self):
        return f'<Reservation hotel: {self.hotel_id}, user_id: {self.user_id}, date: {self.date}>'