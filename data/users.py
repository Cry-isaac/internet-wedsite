import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from forms.user import RegisterForm
from .models import user_reservations
from .db_session import SqlAlchemyBase
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from sqlalchemy import ForeignKey


#Таблица пользователя
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Связи
    hotels = relationship('Hotel', back_populates='owner', cascade='all, delete-orphan')  # Отели, созданные пользователем
    reservations = relationship('BookedDate', back_populates='user', cascade='all, delete-orphan')  # Бронирования пользователя
    reviews = relationship('Review', back_populates='user')


    def __repr__(self):
        return f'<User {self.id}, name={self.name}, about={self.about}, email={self.email}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)