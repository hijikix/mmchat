from common.db_base import Base
from common.db_base import Session

class SqlalchemyPlugin(object):
    name = 'sqlalchemy'
    api = 2

    def __init__(self):
        pass

    def setup(self, app):
        pass

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            try:
                rv = callback(*args, **kwargs)
                print("commit")
                Session.commit()
            except:
                print("rollback")
                Session.rollback()
                raise
            finally:
                print("remove")
                Session.remove()
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper
