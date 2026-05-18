from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class HotelForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField("Описание")
    city = StringField("Город")
    location = StringField("Адрес")
    stars = IntegerField('Звезды')
    price = IntegerField('Цена за ночь')
    submit = SubmitField('Применить')
