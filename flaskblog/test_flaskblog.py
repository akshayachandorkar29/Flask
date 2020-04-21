import requests
import os
from dotenv import load_dotenv
load_dotenv()
import pytest
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Secure


class TestRegistration:

    def test_register(self):
        url = os.getenv("flask_url") + '/register'
        data = {'username': 'sunita', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmail.com'}
        res = requests.post(url=url, data=data)
        print(res.text)
        assert res.status_code == 200


class TestLogin:

    def test_login(self):
        url = os.getenv("flask_url") + '/login'
        data = {'password': 'akshaya', 'email': 'akshayachandorkar29@gmail.com'}
        user = User.query.filter_by(email='akshayachandorkar29@gmail.com').first()
        user.active = 1
        db.session.commit()
        res = requests.post(url=url, data=data)
        print(res.text)
        assert res.status_code == 200


class TestForgot:

    def test_forgot(self):
        url = os.getenv("flask_url") + '/forgot'
        data = {'email': 'akshayachandorkar29@gmail.com'}
        res = requests.post(url=url, data=data)
        print(res.text)
        assert res.status_code == 200