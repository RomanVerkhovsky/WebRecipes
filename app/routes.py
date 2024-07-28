from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Recipe
from urllib.parse import urlsplit


bp = Blueprint('routes', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('routes.index'))


@bp.route('/profile')
@login_required
def profile():

    return render_template('profile.html', title='Profile', name=current_user.username,
                           email=current_user.email)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Неверный адрес электронной почты или пароль!')
            return redirect(url_for('routes.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('routes.profile')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.profile'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Поздравляем, теперь вы зарегистрировались в системе!')

        return redirect(url_for('routes.login'))

    return render_template('register.html', title='Register', form=form)


@bp.route('/recipes', methods=['GET', 'POST'])
def recipes():
    list_recipes = Recipe.query.all()
    return render_template('recipes.html', title="list of recipes", list_recipes=list_recipes)


@bp.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():

    return render_template('new_recipe.html', title="new_recipe")
