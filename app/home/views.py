from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from . import home


@home.route('/')
@home.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.browseCases')) #render_template('home/index.html', title='Home')
    else:
        return redirect(url_for('auth.login'))

@home.route('/help')
@login_required
def help():
    return render_template('home/help.html')

