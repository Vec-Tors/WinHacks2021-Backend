import sanic
from sanic import Sanic
import ujson as json
import datetime
import places_puller

app = Sanic("WinHacks2021-Vectors-Agriculture")

@app.route("/keep_alive")
async def keep_alive(request):
    return sanic.response.text("Online!")

@app.route("/all_data")
async def all_data(request):
    data = json.load(open('data.json', 'r'))
    if (datetime.datetime.now() - datetime.datetime.fromtimestamp(data['summary']['timestamp'])).total_seconds() >= 86400:
        data = places_puller.main()
    return sanic.response.json(data)

app.run(debug=True, port='3000', host='0.0.0.0')