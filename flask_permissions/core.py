
class Permissions(object):

    def __init__(self, app, local_db):
        self.init_app(app, local_db)

    def init_app(self, app, local_db):
        self.app = app
        global db
        db = local_db

import models
