from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
from .core import Permissions
from .models import Role, Ability, UserMixin


class ModelsTests(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        return app
