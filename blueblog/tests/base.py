import unittest

from flask import url_for

from blueblog import create_app
from blueblog.extensions import db
from blueblog.models import Admin


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

        db.create_all()
        user = Admin(name='Grey Li', username='grey', about='I am test', blog_title='Testlog', blog_sub_title='a test')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'grey'
            password = '123'

        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
