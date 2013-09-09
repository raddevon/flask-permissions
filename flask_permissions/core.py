from functools import wraps


class Permissions(object):

    def __init__(self, app, local_db):
        self.init_app(app, local_db)

    def init_app(self, app, local_db):
        self.app = app
        global db
        db = local_db

    def user_has(attribute):
        """
        Takes an attribute (a string name of either a role or an ability) and returns the function if the user has that attribute
        """
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                attribute_object = Role.query.filter_by(name=attribute).first()
                user_abilities = []
                for role in current_user.roles:
                    user_abilities += [
                        role.ability for ability in role.abilities]
                if attribute_object in current_user.roles or attribute_object in user_abilities:
                    return func(*args, **kwargs)
                else:
                    # Make this do someting way better.
                    return "You do not have access"
            return inner
        return wrapper

    def user_is(attribute):
        """
        Takes an attribute (a string name of either a role or an ability) and returns the function if the user has that attribute
        """
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                attribute_object = Ability.query.filter_by(
                    name=attribute).first()
                user_abilities = []
                for role in current_user.roles:
                    user_abilities += [
                        role.ability for ability in role.abilities]
                if attribute_object in current_user.roles or attribute_object in user_abilities:
                    return func(*args, **kwargs)
                else:
                    # Make this do someting way better.
                    return "You do not have access"
            return inner
        return wrapper
