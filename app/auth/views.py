from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user,logout_user, login_required, current_user
from werkzeug.urls import url_parse


from app.auth.emails import send_password_reset_email

from . import auth
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm

from app.database import get_user_salt, set_user_salt, hash_password, get_user_info, create_user, change_password


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        print('user', user)
        if user is None:
            flash('Chybně zadané heslo nebo uživatelské jméno.')
            return redirect(url_for('auth.login'))
        salt = get_user_salt(form.username.data)
        hashed_password = hash_password(salt, form.password.data)
        user_info = get_user_info(form.username.data, hashed_password)
        if user_info is None or salt is None: 
            flash('Chybně zadané heslo nebo uživatelské jméno.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user is None:
            flash('Chybně zadané heslo nebo uživatelské jméno.')
        salt = get_user_salt(form.username.data)
        hashed_password = hash_password(salt, form.password.data)
        user_info = get_user_info(form.username.data, hashed_password)

        if user_info is None or salt is None: 
            flash('Chybně zadané heslo nebo uživatelské jméno.')
        else:
            user_id = user_info[0]
            new_hashed_password = hash_password(salt, form.password2.data)
            new_password = change_password(user_id, new_hashed_password)
            if new_password == 'OK':
                flash('Změna hesla proběhla úspěšně.')
            else:
                flash('Bohužel, změna hesla byla neúspěšná.')

    return render_template('auth/change_password.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
   # if current_user.is_authenticated:
   #     return redirect(url_for('home.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(UserName=form.username.data)
        new_salt = set_user_salt()
        hashed_password = hash_password(new_salt, form.password.data)
        new_user = create_user(
            role=form.role.data, 
            username=form.username.data, 
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            passwordhash=hashed_password,
            passwordsalt=new_salt)
        if new_user == 'OK':
            flash('Registrace proběhla úspěšně.')
            #return redirect(url_for('auth.login'))
        else:
            flash('Bohužel, registrace byla neúspěšná.')

    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)