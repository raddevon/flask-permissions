
try:
    from .core import db
except ImportError:
    raise Exception(
        'Permissions app must be initialized before importing models')

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from .utils import is_sequence


def _role_find_or_create(r):
    role = Role.query.filter_by(name=r).first()
    if not(role):
        role = Role(name=r)
        db.session.add(role)
    return role


def make_user_role_table(table_name='user', id_column_name='id'):
    """
        Create the user-role association table so that
        it correctly references your own UserMixin subclass.

    """

    return db.Table('fp_user_role',
                       db.Column(
                           'user_id', db.Integer, db.ForeignKey('{}.{}'.format(
                               table_name, id_column_name))),
                       db.Column(
                       'role_id', db.Integer, db.ForeignKey('fp_role.id')),
                       extend_existing=True)


role_ability_table = db.Table('fp_role_ability',
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('fp_role.id')),
                              db.Column(
                              'ability_id', db.Integer, db.ForeignKey('fp_ability.id'))
                              )


class Role(db.Model):

    """
    Subclass this for your roles
    """
    __tablename__ = 'fp_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    abilities = db.relationship(
        'Ability', secondary=role_ability_table, backref='roles')

    def __init__(self, name):
        self.name = name.lower()

    def add_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(
                name=ability).first()
            if not existing_ability:
                existing_ability = Ability(ability)
                db.session.add(existing_ability)
                db.session.commit()
            self.abilities.append(existing_ability)

    def remove_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(name=ability).first()
            if existing_ability and existing_ability in self.abilities:
                self.abilities.remove(existing_ability)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __str__(self):
        return self.name


class Ability(db.Model):

    """
    Subclass this for your abilities
    """
    __tablename__ = 'fp_ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)

    def __str__(self):
        return self.name


class UserMixin(db.Model):

    """
    Subclass this for your user class
    """

    __abstract__ = True

    @hybrid_property
    def _id_column_name(self):

        # the list of the class's columns (with attributes like
        # 'primary_key', etc.) is accessible in different places
        # before and after table definition.
        if self.__tablename__ in list(self.metadata.tables.keys()):
            # after definition, it's here
            columns = self.metadata.tables[self.__tablename__]._columns
        else:
            # before, it's here
            columns = self.__dict__

        for k, v in list(columns.items()):
            if getattr(v, 'primary_key', False):
                return k

    @declared_attr
    def _roles(self):
        user_role_table = make_user_role_table(self.__tablename__,
                                               self._id_column_name.fget(self))
        return db.relationship(
            'Role', secondary=user_role_table, backref='users')

    @declared_attr
    def roles(self):
        return association_proxy('_roles', 'name', creator=_role_find_or_create)

    def __init__(self, roles=None, default_role='user'):
        # If only a string is passed for roles, convert it to a list containing
        # that string
        if roles and isinstance(roles, str):
            roles = [roles]

        # If a sequence is passed for roles (or if roles has been converted to
        # a sequence), fetch the corresponding database objects and make a list
        # of those.
        if roles and is_sequence(roles):
            self.roles = roles
        # Otherwise, assign the default 'user' role. Create that role if it
        # doesn't exist.
        elif default_role:
            self.roles = [default_role]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def add_roles(self, *roles):
        self.roles.extend([role for role in roles if role not in self.roles])

    def remove_roles(self, *roles):
        self.roles = [role for role in self.roles if role not in roles]

    def get_id(self):
        return str(getattr(self, self._id_column_name))

    def __repr__(self):
        return '<{} {}>'.format(self.__tablename__.capitalize(), self.get_id())
