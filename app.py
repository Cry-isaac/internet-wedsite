from flask import Flask, render_template, redirect, request
from flask_restful import Api, abort
from sqlalchemy import desc
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.hotels import Hotel
from data import db_session
from data.reservations import BookedDate
from data.users import User
from forms.hotel import HotelForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    #Подключение к бд
    db_session.global_init("db/blogs.db")

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        user = db_sess.get(User, user_id)
        db_sess.close()
        return user

    @app.route('/', methods=['GET', 'POST'])
    def index():
        search_query = request.form.get('city', '')
        db_sess = db_session.create_session()
        try:
            # Обработка POST‑запроса
            if search_query:
                # Получаем данные из формы
                city = request.form.get('city')
                check_in = request.form.get('check_in')
                check_out = request.form.get('check_out')

                # Фильтруем отели по параметрам
                hotels = db_sess.query(Hotel).filter(city == Hotel.city).all()
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
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        user = load_user(current_user.id)
        db_sess = db_session.create_session()
        hotels = db_sess.query(Hotel).filter(Hotel.user_id == user.id).all()
        booked_date = db_sess.query(BookedDate).filter(BookedDate.user_id == user.id).all()
        db_sess.close()
        return render_template('profile.html', user=user, user_hotels=hotels, user_booking=booked_date)

    @app.route('/add_hotel', methods=['GET', 'POST'])
    @login_required
    def add_hotel():
        form = HotelForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.get(User, current_user.id)
            hotel = Hotel()
            # Получаем данные из формы
            hotel.title = form.title.data
            hotel.city = form.city.data
            hotel.location = form.location.data
            hotel.price= form.price.data
            hotel.stars = form.stars.data
            hotel.description = form.description.data
            hotel.user_id = current_user.id
            user.hotel.append(hotel)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/profile')
        return render_template('add_hotel.html', form=form)

    @app.route('/hotel/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_hotel(id):
        form = HotelForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            hotel = db_sess.query(Hotel).filter(Hotel.id == id,
                                              Hotel.user_id == current_user.id
                                              ).first()
            if hotel:
                form.title.data = hotel.title
                form.city.data = hotel.city
                form.location.data = hotel.location
                form.price.data = hotel.price
                form.stars.data = hotel.stars
                form.description.data = hotel.description
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            hotel = db_sess.query(Hotel).filter(Hotel.id == id,
                                              Hotel.user_id == current_user.id
                                              ).first()
            if hotel:
                hotel.title = form.title.data
                hotel.city = form.city.data
                hotel.location = form.location.data
                hotel.price = form.price.data
                hotel.stars = form.stars.data
                hotel.description = form.description.data
                hotel.user_id = current_user.id
                db_sess.commit()
                return redirect('/profile')
            else:
                abort(404)
        return render_template('hotel.html',
                               title='Редактирование отеля',
                               form=form
                               )

    @app.route('/hotel_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def hotel_delete(id):
        db_sess = db_session.create_session()
        hotel = db_sess.query(Hotel).filter(Hotel.id == id,
                                          Hotel.user_id == current_user.id
                                          ).first()
        if hotel:
            db_sess.delete(hotel)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/profile')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    app.run()


if __name__ == '__main__':
    main()