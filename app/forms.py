from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """
    Форма для заполнения данных на вход существующего пользователя
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Форма для заполнения данных на добавление нового пользователя
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь не зарегистрирован! Введите другой email.')


class RecipeForm(FlaskForm):
    """
    Форма для заполнения данных на добавление нового блюда
    """
    title = StringField("Dish", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    ingredients = StringField("Ingredients", validators=[DataRequired()])
    steps = StringField("Steps", validators=[DataRequired()])
    time = StringField("Cook time", validators=[DataRequired()])
    add = SubmitField('Add Recipe')
