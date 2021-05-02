import os
import datetime

from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_ckeditor import CKEditor
from flask import flash, url_for

from data import db_session
from data.users import User
from data.photos import Photos
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.photos import PhotosForm

from werkzeug.utils import secure_filename

from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RTPv?X%OMS8pcDDql{HB'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
login_manager = LoginManager()
login_manager.init_app(app)

# подключаем текстовый редактор CKEditor
ckeditor = CKEditor()
ckeditor.init_app(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['CKEDITOR_SERVE_LOCAL'] = 'True'
app.config['CKEDITOR_HEIGHT'] = 400

# Папка для загрузки изображений
UPLOAD_FOLDER = 'userdata'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.instance_path), 'static')
app.config['UPLOAD_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], UPLOAD_FOLDER)


def make_preview(size, n_colors, filename):  # Делаем миниатюру
    # TODO: надо доделать
    # im = Image.open(filename)
    # im = im.resize(size)
    # im = im.quantize(n_colors)
    # im.save('mini-'+filename)
    return im


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():  # Главная страница
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        photos = db_sess.query(Photos).filter(
            (Photos.user == current_user) | (Photos.is_private != True))
    else:
        photos = db_sess.query(Photos).filter(Photos.is_private != True)
    return render_template("index.html", photos=photos, active1='active')


@app.route('/register', methods=['GET', 'POST'])
def reqister():  # Регистрация
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
def login():  # Вход на сайт
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


@app.route('/logout')
@login_required
def logout():  # Выход с сайта
    logout_user()
    return redirect("/")


@app.route('/photos', methods=['GET', 'POST'])
def myphotos():  # Моиф фотографии
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        photos = db_sess.query(Photos).filter(
            (Photos.user == current_user) | (Photos.is_private != True))
    else:
        photos = db_sess.query(Photos).filter(Photos.is_private != True)

    return render_template("myphotos.html", photos=photos, active2='active')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_photos():  # Добавление новых фотографий
    form = PhotosForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        photos = Photos()
        photos.title = form.title.data
        photos.content = form.content.data
        photos.is_private = form.is_private.data

        # Загрузка файла
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id) + '-' + current_user.name)

        if not os.path.exists(path):
            os.makedirs(path)

        f = form.upload.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(path, filename))
        # f_mini = make_preview((300,300),100,os.path.join(path, filename))
        # f_mini.save(os.path.join(path, filename))
        print(filename)
        print('------------')

        photos.filename = filename

        current_user.photos.append(photos)

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('photos_add.html', title='Добавление фотографий', form=form, active3='active')


@app.route('/photos_add/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_photos(id):  # Изменение фотки
    form = PhotosForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        photos = db_sess.query(Photos).filter(Photos.id == id,
                                              Photos.user == current_user
                                              ).first()
        if photos:
            form.title.data = photos.title
            form.content.data = photos.content
            form.is_private.data = photos.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        photos = db_sess.query(Photos).filter(Photos.id == id,
                                              Photos.user == current_user
                                              ).first()
        if photos:
            photos.title = form.title.data
            photos.content = form.content.data
            photos.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('photos_add.html',
                           title='Редактирование фотографию',
                           form=form
                           )


@app.route('/photos_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def photos_delete(id):  # Удаление фотографии
    db_sess = db_session.create_session()
    photos = db_sess.query(Photos).filter(Photos.id == id,
                                          Photos.user == current_user
                                          ).first()
    if photos:
        db_sess.delete(photos)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/photos_show/<int:id>', methods=['GET', 'POST'])
def photos_show(id):  # Показать фотографию
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        photos = db_sess.query(Photos).filter(
            (Photos.user == current_user) | (Photos.is_private != True))
    else:
        photos = db_sess.query(Photos).filter(Photos.is_private != True)
    return render_template('photos_show.html', title='Отображение фотографии', photos=photos, id=id)


@app.route('/editor', methods=['GET', 'POST'])
@login_required
def editor():  # Редактор текста
    # TODO: можно добавить в редактор профиля
    return render_template('editor.html',
                           title='Редактор')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():  # Настройки профиля
    return render_template('settings.html',
                           title='Найстройки', active4='active')


def main():
    db_session.global_init("db/database.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
