from functools import wraps


def import_user():
    """
    Attempts to import the Flask-Login current_user proxy

    Returns:
        The Flask-Login current_user proxy.
    """
    try:
        from flask.ext.login import current_user
        return current_user
    except ImportError:
        raise ImportError(
            'User argument not passed and Flask-Login current_user could not be imported.')


def user_has(ability, user=None):
    """
    Prevents access to a route unless the user has the given ability.

    Args:
        ability: The string name of the ability to test.
        user: (Optional) The user object to test for the given ability. If omitted, the function will attempt to import the Flask-Login current_user.
    Returns:
        The decorated function.
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from .models import Ability
            desired_ability = Ability.query.filter_by(
                name=ability).first()
            user_abilities = []
            current_user = user or import_user()
            try:
                for role in current_user.roles:
                    user_abilities += [
                        role.ability for a in role.abilities]
            except AttributeError:
                pass
            if desired_ability in user_abilities:
                return func(*args, **kwargs)
            else:
                return "You do not have access", 403
        return inner
    return wrapper


def user_is(role, user=None):
    """
        Prevents access to a route unless the user has the given role.

        Args:
            role: The string name of the role to test.
            user: (Optional) The user object to test for the given role. If omitted, the function will attempt to import the Flask-Login current_user.
        Returns:
            The decorated function.
        """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from .models import Role
            desired_role = Role.query.filter_by(
                name=role).first()
            current_user = user or import_user()
            try:
                if desired_role in current_user.roles:
                    return func(*args, **kwargs)
            except AttributeError:
                pass
            return "You do not have access", 403
        return inner
    return wrapper
