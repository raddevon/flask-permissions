from flask import Flask
import unittest
from flask.ext.testing import TestCase as FlaskTestCase
from flask.ext.sqlalchemy import SQLAlchemy
from .core import Permissions
from .utils import is_sequence
from .decorators import user_has, user_is
from werkzeug.exceptions import Forbidden
import os

app = Flask(__name__)
app.config['TESTING'] = True

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)

perms = Permissions(app, db, None)

from .models import Role, Ability, UserMixin


class DatabaseTests(FlaskTestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        os.remove(db_path)


class ModelsTests(DatabaseTests):

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
        self.assertItemsEqual(new_roles, test_user.roles)

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
        self.assertItemsEqual(new_roles, test_user.roles)

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
        self.assertItemsEqual(test_user.roles, ['superadmin'])

    def test_add_abilities_with_nonexisting_abilities(self):
        role = Role('admin')
        new_abilities = ['create_users', 'set_roles', 'set_abilities']
        role.add_abilities(*new_abilities)
        db.session.add(role)
        db.session.commit()
        test_role = Role.query.get(1)
        abilities = [ability.name for ability in test_role.abilities]
        self.assertItemsEqual(new_abilities, abilities)

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
        self.assertItemsEqual(new_abilities, abilities)

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
        self.assertItemsEqual(abilities, ['create_users'])


class DecoratorsTests(DatabaseTests):

    def mock_function(self):
        return True

    def create_user(self):
        role = Role('admin')
        new_abilities = ['create_users', 'set_roles', 'set_abilities']
        for ability in new_abilities:
            new_ability = Ability(ability)
            db.session.add(new_ability)
            db.session.commit()
        role.add_abilities(*new_abilities)
        db.session.add(role)
        db.session.commit()

        user = UserMixin(roles='admin')
        db.session.add(user)
        db.session.commit()

    def return_user(self):
        user = UserMixin.query.get(1)
        return user

    def setUp(self):
        super(DecoratorsTests, self).setUp()
        self.create_user()

    def test_user_has_pass(self):
        wrapped_function = user_has(
            'create_users', self.return_user)(self.mock_function)
        self.assertTrue(wrapped_function())

    def test_user_has_fail(self):
        wrapped_function = user_has(
            'edit', self.return_user)(self.mock_function)
        self.assertRaises(Forbidden, wrapped_function)

    def test_user_is_pass(self):
        wrapped_function = user_is(
            'admin', self.return_user)(self.mock_function)
        self.assertTrue(wrapped_function())

    def test_user_is_fail(self):
        wrapped_function = user_is(
            'user', self.return_user)(self.mock_function)
        self.assertRaises(Forbidden, wrapped_function)


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
