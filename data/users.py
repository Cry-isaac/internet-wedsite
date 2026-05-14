import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from sqlalchemy import ForeignKey


#Таблица пользователя
class User(SqlAlchemyBase):
    #Название таблицы
    __tablename__ = 'users'

    #Столбцы
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    reservations_id = sqlalchemy.Column(sqlalchemy.DateTime, ForeignKey('reservations.id'), nullable=True)

    #Отношения
    hotel = relationship("Hotel", back_populates='user')
    review = relationship("Review", back_populates='user')
    # booked_date = orm.relationship('BookedDate', secondary=association_table_user, back_populates='user')

    def __repr__(self):
        return f'<User {self.id}, name={self.name}, about={self.about}, email={self.email}>'

