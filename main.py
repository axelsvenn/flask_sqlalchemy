import json
from data import db_session
from flask import Flask, render_template, redirect

from data.jobs import Jobs
from forms.loginform import LoginForm
from forms.user import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.is_private != True)
    return render_template("index.html", news=news)


@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Riddley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user = User()
    user.surname = "White"
    user.name = "Walter"
    user.age = 52
    user.position = "cook"
    user.speciality = "cook our food"
    user.address = "module_kitchen"
    user.email = "savewalterwhite@mars.org"
    user.set_password("heisenberg")
    db_sess.add(user)

    user = User()
    user.surname = "Sadovnikov"
    user.name = "Sergei"
    user.age = 35
    user.position = "programmer"
    user.speciality = "rostelecom"
    user.address = "module_208"
    user.email = "sersad@mars.org"
    user.set_password("sersad")
    db_sess.add(user)

    user = User()
    user.surname = "Ivanov"
    user.name = "Grisha"
    user.age = 17
    user.position = "clown"
    user.speciality = "lyceum_yandex"
    user.address = "module_208"
    user.email = "mulgach@mars.org"
    user.set_password("mulgach2005")
    db_sess.add(user)

    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()