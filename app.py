from datetime import datetime

from flask import Flask, render_template, redirect, request, flash
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
    # Подключение к бд
    db_session.global_init("db/blogs.db")

    def calculate_nights(check_in_str, check_out_str):

        #Вычисляет количество ночей между датами заезда и выезда.

        check_in = datetime.strptime(check_in_str, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d')

        # Разница в днях
        nights = (check_out - check_in).days

        if nights < 0:
            raise ValueError("Дата выезда не может быть раньше даты заезда")
        if nights == 0:
            raise ValueError("Минимальное бронирование — 1 ночь")

        return nights

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        user = db_sess.get(User, user_id)
        db_sess.close()
        return user

    @app.route('/', methods=['GET', 'POST'])
    def index():
        db_sess = db_session.create_session()
        city = ''  # По умолчанию
        error = ''

        try:
            if request.method == 'POST':
                form_type = request.form.get('form_type')
                # Получается город
                if form_type == 'search' or 'search' in request.form:
                    city = request.form.get('city', '').strip()

                    # Строим запрос с фильтрацией, если город указан
                    if city:
                        hotels = db_sess.query(Hotel).filter(Hotel.city.ilike(f'%{city}%')).order_by(desc(Hotel.stars)).all()
                    else:
                        # Если город не указан, показываем все отели
                        hotels = db_sess.query(Hotel).order_by(desc(Hotel.stars)).all()
                else:  # GET‑запрос. Показываются все отели
                    hotels = db_sess.query(Hotel).order_by(desc(Hotel.stars)).all()
            else:
                hotels = db_sess.query(Hotel).order_by(desc(Hotel.stars)).all()
            return render_template(
                'index.html',
                hotels=hotels,
                city=city,
                error=error
            )


        except Exception:
            # Показывается сообщение об ошибке в шаблоне
            return render_template(
                'index.html',
                hotels=[],
                city=city,
                error="Произошла ошибка при загрузке данных"
            )
        finally:
            db_sess.close()

    @app.route('/booking', methods=['POST'])
    def booking():
        db_sess = db_session.create_session()
        error = ''
        hotels = db_sess.query(Hotel).order_by(desc(Hotel.stars)).all()
        print(hotels[0].id)
        if not current_user or not current_user.is_authenticated:
            print('не вошел')
            error = 'Для бронирования необходимо войти в аккаунт'
        else:
            reservation = BookedDate()
            user = db_sess.get(User, current_user.id)
            hotel_id = request.form.get('hotel_id')
            check_in = request.form.get('check_in')
            check_out = request.form.get('check_out')
            hotel = db_sess.get(Hotel, hotel_id)
            nights = calculate_nights(check_in, check_out)

            reservation.hotel_id = hotel_id
            reservation.user_id = user.id
            reservation.pet_name = request.form.get('pet_name')
            reservation.check_in = datetime.strptime(check_in, '%Y-%m-%d')
            reservation.check_out = datetime.strptime(check_out, '%Y-%m-%d')
            reservation.total_price = nights * hotel.price
            print(type(check_out))

            user.reservations.append(reservation)
            hotel.reservations.append(reservation)
            db_sess.merge(current_user)
            db_sess.commit()
        return render_template(
                'index.html',
                hotels=hotels,
                city='',
                error=error
            )

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
        hotels = db_sess.query(Hotel).filter(Hotel.owner_id == user.id).all()
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
            hotel.price = form.price.data
            hotel.stars = form.stars.data
            hotel.description = form.description.data
            hotel.user_id = current_user.id
            user.hotels.append(hotel)
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
                                                Hotel.owner_id == current_user.id
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
                                                Hotel.owner_id == current_user.id
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
                                            Hotel.owner_id == current_user.id
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
