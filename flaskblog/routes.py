"""
This is the file where all the routes are there
Author: Akshaya Revaskar
Date: 12/04/2020
"""
from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog import app, db, bcrypt
from flask_mail import Message
from flaskblog.forms import RegistrationForm, LoginForm, ForgotForm, ResetForm
from flaskblog.models import User, Secure
import jwt
import os
from flaskblog.short_url_generator import ShortUrlGenerator
from flaskblog.send_mail import SendMail
from flaskblog.redis_service import RedisService
from dotenv import load_dotenv
load_dotenv()

redis_obj = RedisService()
short_object = ShortUrlGenerator()
mail_object = SendMail()

posts = [
    {
        'author': 'Akshaya Revaskar',
        'title': 'Register',
        'content': 'API for registering new user',
        'date_posted': 'April 10, 2021'
    },
    {
        'author': 'Chetan Revakar',
        'title': 'Login',
        'content': 'API for login registered user',
        'date_posted': 'April 10, 2021'
    },
{
        'author': 'Saurabh Kalan',
        'title': 'Forgot',
        'content': 'API for resetting password in case user forgot',
        'date_posted': 'April 10, 2021'
    },
{
        'author': 'Sarvesh Patil',
        'title': 'Reset',
        'content': 'API for resetting the password',
        'date_posted': 'April 10, 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()

        db_id = user.id

        # generating token using JWT module
        token = jwt.encode({'id': db_id}, 'secret', algorithm='HS256').decode('utf-8')

        short = short_object.short_url(10)

        secure = Secure(token=token, short=short)
        db.session.add(secure)
        db.session.commit()

        url = os.getenv("flask_url")

        # message to send in the mail as a link
        msg = Message('Link', sender=os.getenv("Flask_MAIL_USERNAME"), recipients=['akshayachandorkar29@gmail.com'])
        msg.body = f"Click here to activate : {url}/activate/token={short}"

        # sending mail using token and link
        mail_object.send_mail(msg)

        flash('Your account has been created... Link has been mailed to you for activation... '
              'Please activate to login!!!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/activate/token=<string:token>/')
def activate(token):
    # getting token from short url in mail
    secure = Secure.query.filter_by(short=token).first()
    l_token = secure.token

    # decoding token to get user id
    payload = jwt.decode(l_token, 'secret', algorithms=['HS256'])
    user_id = payload.get('id')

    # activating user by updating User table
    user = User.query.filter_by(id=user_id).first()
    user.active = 1
    db.session.commit()

    return render_template('activate.html', token=token)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password) and user.active == 1:
            user_id = user.id
            # generating token using JWT module
            token = jwt.encode({'id': user_id}, 'secret', algorithm='HS256').decode('utf-8')

            # setting data into redis cache
            redis_obj.set(user_id, token)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password or you have not activated yourself.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        user = User.query.filter_by(email=email).first()

        db_id = user.id

        # generating token with JWT module
        token = jwt.encode({'id': db_id}, 'secret', algorithm='HS256').decode('utf-8')

        short = short_object.short_url(10)

        secure = Secure(token=token, short=short)
        db.session.add(secure)
        db.session.commit()

        url = os.getenv("flask_url")

        # message to send in the mail as a link
        msg = Message('Link', sender=os.getenv("Flask_MAIL_USERNAME"), recipients=['akshayachandorkar29@gmail.com'])
        msg.body = f"Click here to activate : {url}/reset/token={short}"

        # sending mail using token and link
        mail_object.send_mail(msg)
        flash('Email has been send to you for reset... Please click on it to reset password', 'success')
    return render_template('forgot.html', title='Forgot', form=form)


@app.route('/reset/token=<string:token>/', methods=['GET', 'POST'])
def reset(token):
    form = ResetForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        # getting token from short url in mail
        secure = Secure.query.filter_by(short=token).first()
        l_token = secure.token

        # decoding token to get user id
        payload = jwt.decode(l_token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # resetting password
        user = User.query.filter_by(id=user_id).first()
        user.password = hashed_password
        db.session.commit()
        flash('Your Password Reset Successful', 'success')
    return render_template('reset.html', title='Reset', form=form, token=token)
