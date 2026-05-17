from flask import Flask, render_template, redirect, jsonify, request
from flask_restful import Api
from sqlalchemy import desc

from data.hotels import Hotel
from data import db_session
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    #Подключение к бд
    db_session.global_init("db/blogs.db")

    @app.route('/', methods=['GET', 'POST'])
    def index():
        db_sess = db_session.create_session()
        try:
            # Обработка POST‑запроса
            if request.method == 'POST':
                # Получаем данные из формы
                location = request.form.get('location', '')
                check_in = request.form.get('check_in')
                check_out = request.form.get('check_out')

                # Фильтруем отели по параметрам
                hotels = db_sess.query(Hotel).filter(
                    Hotel.location.contains(location)
                ).all()
            else:
                # Для GET‑запроса показываем все отели
                hotels = db_sess.query(Hotel).order_by(desc(Hotel.stars)).all()

            return render_template('index.html', hotels=hotels)
        finally:
            # Обязательно закрываем сессию БД
            db_sess.close()

    # Регистрация
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')

    app.run()


if __name__ == '__main__':
    main()