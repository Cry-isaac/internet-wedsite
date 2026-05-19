from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ReservationsForm(FlaskForm):
    pet_name = StringField('Название', validators=[DataRequired()])
    check_in = DataRequired()
    check_out = DataRequired()
    submit = SubmitField('Применить')
