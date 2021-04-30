from flask import Flask, render_template, redirect, request, make_response, session
from data import db_session
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.users import User
from data.news import News
# from forms.user import RegisterForm
# from forms.login import LoginForm
# from forms.news import NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RTPv?X%OMS8pcDDql{HB'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)

    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)

    return render_template("index.html", news=news, active1='active')



def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()