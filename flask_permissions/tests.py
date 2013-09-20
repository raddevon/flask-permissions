from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
from .core import Permissions
import os


class ModelsTests(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.db_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            self.db_path
        self.db = SQLAlchemy()
        self.db.init_app(app)
        perms = Permissions(app, self.db, None)
        from .models import Role, Ability, UserMixin
        return app

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        os.remove(self.db_path)

    def test_user_mixin(self):
        from .models import UserMixin
        user = UserMixin()
        self.db.session.add(user)
        self.db.session.commit()
        self.assertEqual(user.id, 1)
