from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


from flask_ckeditor import CKEditorField


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    # content = TextAreaField("Содержание")
    content = CKEditorField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')