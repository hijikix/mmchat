import uuid
from bottle import Bottle, run

from plugin.bottle_sqlalchemy import SqlalchemyPlugin
from module.station import StationApi
from module.security import SecurityApi

sqlalchemy = SqlalchemyPlugin()

app = Bottle()
app.install(sqlalchemy)


@app.route('/hello')
def hello():
    lon = 139.728001
    lat = 35.628832
    distance = 5
    nearest_stations = StationApi.get_nearest_stations(lon, lat, 3, distance)
    return "Hello World!"

@app.route('/auth')
def auth():
    from module.security import SecurityApi, PRIVATE_KEY, PUBLIC_KEY
    user_id = str(uuid.uuid4()).encode('utf-8')
    aes_key = b"039D40E223EBE14D5B844FA476786390"
    encrypted_user_id = SecurityApi.rsa_encrypt(PUBLIC_KEY, user_id)
    encrypted_aes_key = SecurityApi.rsa_encrypt(PUBLIC_KEY, aes_key)

    user_auth = SecurityApi.authorize(
        encrypted_user_id, encrypted_aes_key)
    return "auth"

run(app, host='localhost', port=8080)
