class Permissions(object):

    """
    Grabs data from the developer needed for the functionality of the Flask-Permissions extension
    """

    def __init__(self, app, local_db, current_user):
        """
        Initializes the object getting the necessary data about the Flask app from the developer

        Args:
            app: The Flask app.
            local_db: The Flask-SQLAlchemy database object.
            current_user: A proxy to the currently logged in user.
        """
        self.init_app(app, local_db, current_user)

    def init_app(self, app, local_db, current_user):
        self.app = app
        self.current_user = current_user
        global db
        db = local_db
