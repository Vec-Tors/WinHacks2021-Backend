import sanic
from sanic import Sanic
from sanic import Blueprint
import ujson as json
import datetime
import places_puller
from sanic_cors import CORS, cross_origin
import image_map

app = Sanic("WinHacks2021-Vectors-Agriculture")
CORS(app)

@app.route("/keep_alive")
async def keep_alive(request):
    return sanic.response.text("Online!")

@app.route("/all_data")
async def all_data(request):
    data = json.load(open('data.json', 'r'))
    if (datetime.datetime.now() - datetime.datetime.fromtimestamp(data['summary']['timestamp'])).total_seconds() >= 86400:
        data = places_puller.main()
    return sanic.response.json(data)

@app.route("/municipalities")
async def municipalities(request):
    data = json.load(open('data.json', 'r'))
    if (datetime.datetime.now() - datetime.datetime.fromtimestamp(data['summary']['timestamp'])).total_seconds() >= 86400:
        data = places_puller.main()
    municipalities = []
    for x in data['results']:
        if x['municipality'] not in municipalities:
            municipalities.append(x['municipality'])
    return sanic.response.json(municipalities)

@app.route("/map")
async def serve_map(request):
    data = json.load(open('data.json', 'r'))
    if (datetime.datetime.now() - datetime.datetime.fromtimestamp(data['summary']['timestamp'])).total_seconds() >= 86400:
        data = places_puller.main()

    coordinates = []
    for x in data['results']:
        coordinates.append(
            [x['position']['lat'], x['position']['lon']]
        )
    image_map.generate_map(coordinates)
    static_file_bp = Blueprint('static', url_prefix='/maps')
    static_file_bp.static('/static', './static/maps', name='maps')

    return sanic.response.text(app.url_for('static', name='maps', filename='map.png'))

app.run(debug=True, port='3000', host='0.0.0.0')