from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
from .core import Permissions
import os

app = Flask(__name__)
app.config['TESTING'] = True

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)

perms = Permissions(app, db, None)

from .models import Role, Ability, UserMixin


class ModelsTests(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        os.remove(db_path)

    def test_user_mixin(self):
        user = UserMixin()
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)

    def test_role(self):
        role = Role('admin')
        db.session.add(role)
        db.session.commit()
        self.assertEqual(role.id, 1)

    def test_ability(self):
        ability = Ability('add users')
        db.session.add(ability)
        db.session.commit()
        self.assertEqual(ability.id, 1)

    def test_add_role(self):
        user = UserMixin()
        new_roles = ['admin', 'user', 'superadmin']
        user.add_roles(*new_roles)
        db.session.add(user)
        db.session.commit()
        test_user = UserMixin.query.get(1)
        roles = [role.name for role in test_user.roles]
        self.assertEqual(set(new_roles), set(roles))

