from functools import wraps


def user_has(ability, user=None):
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
            for role in self.current_user.roles:
                user_abilities += [
                    role.ability for a in role.abilities]
            if desired_ability in user_abilities:
                return func(*args, **kwargs)
            else:
                # Make this do someting way better.
                return "You do not have access"
        return inner
    return wrapper


def user_is(role, user=None):
    """
    Takes an role (a string name of either a role or an ability) and returns the function if the user has that role
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from .models import Role
            desired_role = Role.query.filter_by(
                name=attribute).first()
            if desired_role in self.current_user.roles:
                return func(*args, **kwargs)
            else:
                # Make this do someting way better.
                return "You do not have access"
        return inner
    return wrapper
