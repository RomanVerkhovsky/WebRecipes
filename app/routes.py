from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.forms import LoginForm, RegistrationForm, RecipeForm
from app.models import User, Recipe
from urllib.parse import urlsplit


bp = Blueprint('routes', __name__)


@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Проверка введенных данных и вход существующего пользователя
    :return:
    """
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


@bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('routes.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Проверка данных н регистрацию и добавление в базу данных нового пользователя
    :return:
    """
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


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Отображение страницы профиля, проверка нажатия кнопки удаления и удаление рецепта с базы данных
    :return:
    """

    # проверка нажатия кнопки удаления и удаление рецепта с базы данных
    if request.args.get('delete') == "delete":

        recipe_id = request.args.get('recipe')

        recipe_on_del = Recipe.query.filter_by(id=int(recipe_id)).first()

        db.session.delete(recipe_on_del)
        db.session.commit()

    # считывание всех рецептов с бд и передача на html страницу для отображения
    list_recipes = Recipe.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', title='Profile', name=current_user.username,
                           email=current_user.email, list_recipes=list_recipes)


@bp.route('/settings', methods=['GET', 'POST'])
def settings():

    return render_template('settings.html', title="Settings", user=current_user)


@bp.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    """
    Добавление нового рецепта
    :return:
    """

    form = RecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, category=form.category.data, ingredients=form.ingredients.data,
                        steps=form.steps.data, time=form.time.data, user_id=current_user.id)

        db.session.add(recipe)
        db.session.commit()

        flash('Блюдо успешно добавлено в список рецептов!')

        return redirect(url_for('routes.profile'))

    return render_template('new_recipe.html', title="new_recipe", form=form)


@bp.route('/recipe', methods=['GET', 'POST'])
def recipe():
    """
    Отображение нового рецепта
    :return:
    """

    recipe_id = request.args.get('recipe')

    current_recipe = Recipe.query.filter_by(id=int(recipe_id)).first()

    return render_template('recipe.html', title='recipe', recipe=current_recipe)
