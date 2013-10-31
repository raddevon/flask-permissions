from flask import Flask
import unittest
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
from .core import Permissions
from .utils import is_sequence
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

    def test_new_user_with_roles_assigned(self):
        roles = ['admin', 'superadmin']
        for role in roles:
            new_role = Role(role)
            db.session.add(new_role)
            db.session.commit()
        user = UserMixin(roles=roles, default_role=None)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)

    def test_new_user_with_a_single_role_assigned(self):
        new_role = Role('admin')
        db.session.add(new_role)
        db.session.commit()
        user = UserMixin(roles='admin', default_role=None)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)

    def test_user_is_authenticated(self):
        user = UserMixin()
        self.assertTrue(user.is_authenticated())

    def test_user_is_active(self):
        user = UserMixin()
        self.assertTrue(user.is_active())

    def test_user_is_not_anonymous(self):
        user = UserMixin()
        self.assertFalse(user.is_anonymous())

    def test_user_get_id(self):
        user = UserMixin()
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.get_id(), unicode(1))

    def test_user_repr(self):
        user = UserMixin()
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.__repr__(), '<User 1>')

    def test_role(self):
        role = Role('admin')
        db.session.add(role)
        db.session.commit()
        self.assertEqual(role.id, 1)

    def test_role_repr(self):
        role = Role('admin')
        self.assertEqual(role.__repr__(), '<Role admin>')

    def test_role_str(self):
        role = Role('admin')
        self.assertEqual(role.__str__(), 'admin')

    def test_ability(self):
        ability = Ability('create_users')
        db.session.add(ability)
        db.session.commit()
        self.assertEqual(ability.id, 1)

    def test_ability_repr(self):
        ability = Ability('create_users')
        self.assertEqual(ability.__repr__(), '<Ability create_users>')

    def test_ability_repr(self):
        ability = Ability('create_users')
        self.assertEqual(ability.__str__(), 'create_users')

    def test_add_roles_with_nonexisting_roles(self):
        user = UserMixin(default_role=None)
        new_roles = ['admin', 'superadmin', 'editor']
        user.add_roles(*new_roles)
        db.session.add(user)
        db.session.commit()
        test_user = UserMixin.query.get(1)
        roles = [role.name for role in test_user.roles]
        self.assertEqual(set(new_roles), set(roles))

    def test_add_roles_with_existing_roles(self):
        user = UserMixin(default_role=None)
        new_roles = ['admin', 'superadmin', 'editor']
        for role in new_roles:
            new_role = Role(role)
            db.session.add(new_role)
            db.session.commit()
        user.add_roles(*new_roles)
        db.session.add(user)
        db.session.commit()
        test_user = UserMixin.query.get(1)
        roles = [role.name for role in test_user.roles]
        self.assertEqual(set(new_roles), set(roles))

    def test_remove_roles(self):
        user = UserMixin()
        new_roles = ['admin', 'user', 'superadmin']
        user.add_roles(*new_roles)
        db.session.add(user)
        db.session.commit()
        role_remove_user = UserMixin.query.get(1)
        role_remove_user.remove_roles('user', 'admin')
        db.session.add(user)
        db.session.commit()
        test_user = UserMixin.query.get(1)
        roles = [role.name for role in test_user.roles]
        self.assertEqual(set(roles), set(['superadmin']))

    def test_add_abilities_with_nonexisting_abilities(self):
        role = Role('admin')
        new_abilities = ['create_users', 'set_roles', 'set_abilities']
        role.add_abilities(*new_abilities)
        db.session.add(role)
        db.session.commit()
        test_role = Role.query.get(1)
        abilities = [ability.name for ability in test_role.abilities]
        self.assertEqual(set(new_abilities), set(abilities))

    def test_add_abilities_with_existing_abilities(self):
        role = Role('admin')
        new_abilities = ['create_users', 'set_roles', 'set_abilities']
        for ability in new_abilities:
            new_ability = Ability(ability)
            db.session.add(new_ability)
            db.session.commit()
        role.add_abilities(*new_abilities)
        db.session.add(role)
        db.session.commit()
        test_role = Role.query.get(1)
        abilities = [ability.name for ability in test_role.abilities]
        self.assertEqual(set(new_abilities), set(abilities))

    def test_remove_abilities(self):
        role = Role('admin')
        new_abilities = ['create_users', 'set_roles', 'set_abilities']
        role.add_abilities(*new_abilities)
        db.session.add(role)
        db.session.commit()
        ability_remove_role = Role.query.get(1)
        ability_remove_role.remove_abilities('set_roles', 'set_abilities')
        db.session.add(ability_remove_role)
        db.session.commit()
        test_role = Role.query.get(1)
        abilities = [ability.name for ability in test_role.abilities]
        self.assertEqual(set(abilities), set(['create_users']))


class UtilsTests(unittest.TestCase):

    def test_is_string_a_sequence(self):
        string_var = 'This is a string. It is not a sequence.'
        self.assertFalse(is_sequence(string_var))

    def test_is_integer_a_sequence(self):
        int_var = 1
        self.assertFalse(is_sequence(int_var))

    def test_is_bool_a_sequence(self):
        bool_var = True
        self.assertFalse(is_sequence(bool_var))

    def test_is_list_a_sequence(self):
        list_var = [1, 2, 3]
        self.assertTrue(is_sequence(list_var))

    def test_is_set_a_sequence(self):
        set_var = set([1, 2, 3])
        self.assertTrue(is_sequence(set_var))

    def test_is_tuple_a_sequence(self):
        tuple_var = (1, 2, 3)
        self.assertTrue(is_sequence(tuple_var))

    def test_is_dict_a_sequence(self):
        dict_var = {'a': 1, 'b': 2, 'c': 3}
        self.assertTrue(is_sequence(dict_var))
