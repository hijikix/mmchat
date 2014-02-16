from bottle import Bottle, run
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

from common.db_base import Base
from settings import CREATE_ENGINE_URL, CREATE_ENGINE_CONF


engine = create_engine(CREATE_ENGINE_URL, **CREATE_ENGINE_CONF)
plugin = sqlalchemy.Plugin(engine,
                           Base.metadata,
                           keyword='session',
                           create=True,
                           commit=True,
                           use_kwargs=False)

app = Bottle()
app.install(plugin)


@app.route('/hello')
def hello(session):
    return "Hello World!"

run(app, host='localhost', port=8080)
