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
        self.db = SQLAlchemy(app)
        perms = Permissions(app, self.db, None)
        from .models import Role, Ability, UserMixin
        return app

    def setUp(self):
        self.create_app()
        self.db.create_all()

    def tearDown(self):
        os.remove(self.db_path)

    def test_user_mixin(self):
        from .models import UserMixin
        user = UserMixin()
        self.db.session.add(user)
        self.db.session.commit()
        self.assertEqual(user.id, 1)

    def test_role(self):
        from .models import Role
        role = Role('admin')
        self.db.session.add(role)
        self.db.session.commit()
        self.assertEqual(role.id, 1)

    def test_ability(self):
        from .models import Ability
        ability = Ability('add users')
        self.db.session.add(ability)
        self.db.session.commit()
        self.assertEqual(ability.id, 1)

    def test_add_role(self):
        from .models import UserMixin, Role
        user = UserMixin()
        new_roles = ['admin', 'user', 'superadmin']
        user.add_roles(*new_roles)
        self.db.session.add(user)
        self.db.session.commit()
        test_user = UserMixin.get(1)
        roles = [role.name for role in test_user.roles]
        self.assertEqual(set(new_roles), set(roles))
