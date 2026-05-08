from flask import Flask, render_template, redirect
from flask_restful import reqparse, abort, Api, Resource
from forms.user import RegisterForm
from data import db_session


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()