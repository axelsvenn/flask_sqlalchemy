from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")

    user = User()
    user.name = "Пользователь 5"
    user.about = "биография пользователя 5"
    user.email = "email5@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()