from flask import render_template, flash, redirect, request, url_for, current_app
from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('auth/reset_password_text.txt',
                                         user=user, token=token),
               html_body=render_template('auth/reset_password_text.html',
                                         user=user, token=token))