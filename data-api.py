import sanic
from sanic import Sanic
import ujson as json
import datetime
import places_puller
from sanic_cors import CORS, cross_origin

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

app.run(debug=True, port='3000', host='0.0.0.0')