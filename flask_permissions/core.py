class Permissions(object):

    def __init__(self, app, local_db, current_user):
        self.init_app(app, local_db, current_user)

    def init_app(self, app, local_db, current_user):
        self.app = app
        self.current_user = current_user
        global db
        db = local_db
