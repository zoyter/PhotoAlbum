from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

from flask_ckeditor import CKEditorField

from flask_wtf.file import FileField, FileAllowed, FileRequired

class PhotosForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = CKEditorField("Описание")
    # filename = FileField("Файл")
    upload = FileField('Фотография', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Только изображения')
    ])
    is_private = BooleanField("Личное")

    submit = SubmitField('Сохранить')