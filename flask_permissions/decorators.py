from functools import wraps
from werkzeug.exceptions import Forbidden


def import_user():
    try:
        from flask.ext.login import current_user
        return current_user
    except ImportError:
        raise ImportError(
            'User argument not passed and Flask-Login current_user could not be imported.')


def user_has(ability, get_user=import_user):
    """
    Takes an ability (a string name of either a role or an ability) and returns the function if the user has that ability
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from .models import Ability
            desired_ability = Ability.query.filter_by(
                name=ability).first()
            user_abilities = []
            current_user = get_user()
            try:
                for role in current_user.roles:
                    user_abilities += [
                        role.ability for a in role.abilities]
            except AttributeError:
                pass
            if desired_ability in user_abilities:
                return func(*args, **kwargs)
            else:
                raise Forbidden("You do not have access")
        return inner
    return wrapper


def user_is(role, get_user=import_user):
    """
    Takes an role (a string name of either a role or an ability) and returns the function if the user has that role
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from .models import Role
            desired_role = Role.query.filter_by(
                name=role).first()
            current_user = get_user()
            try:
                if desired_role in current_user.roles:
                    return func(*args, **kwargs)
            except AttributeError:
                pass
            raise Forbidden("You do not have access")
        return inner
    return wrapper
