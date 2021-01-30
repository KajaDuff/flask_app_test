from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models import User
class LoginForm(FlaskForm):
    username = StringField('Uživatelské jméno', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember_me = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit se')

class RegistrationForm(FlaskForm):
    role = SelectField('Role', choices=[("Výchozí", "Výchozí")], default="Výchozí", validators=[DataRequired()]) 
    username = StringField('Uživatelské jméno', validators=[DataRequired()])
    firstname = StringField('Křestní jméno', validators=[DataRequired()])
    lastname = StringField('Příjmení', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    password2 = PasswordField(
        'Zopakuj heslo', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrovat se')

    def validate_username(self, username):
        user = User.query.filter_by(UserName=username.data).first()
        if user is not None:
            raise ValidationError('Prosím zvolte jiné užívatelské jméno.')
class ChangePasswordForm(FlaskForm):
    username = StringField('Uživatelské jméno', validators=[DataRequired()])
    password = PasswordField('Staré heslo', validators=[DataRequired()])
    password2 = PasswordField(
        'Nové heslo', validators=[DataRequired()])
    password3 = PasswordField(
        'Zopakuj nové heslo', validators=[DataRequired(), EqualTo('password2')])
    submit = SubmitField('Změnit heslo')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Zažádat změnu hesla')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')