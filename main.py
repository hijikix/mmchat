from bottle import Bottle, run

from module.station import StationApi

app = Bottle()


@app.route('/hello')
def hello():
    lon = 139.728001
    lat = 35.628832
    distance = 5
    nearest_stations = StationApi.get_nearest_stations(lon, lat, 3, distance)
    return "Hello World!"

run(app, host='localhost', port=8080)
