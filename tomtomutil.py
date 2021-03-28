import urllib.parse
import requests
import json

class TomTom:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fuzzySearch(self, query: str, ext: str = "json", **kwargs):
        kwargs['key'] = self.api_key

        r = requests.get(f"https://api.tomtom.com/search/2/search/{urllib.parse.quote(query)}.{ext}?{urllib.parse.urlencode(kwargs)}")
        r.raise_for_status()
        return json.loads(r.content)

    def detailSearch(self, poi_id: str, ext: str = "json", **kwargs):
        kwargs['key'] = self.api_key
        kwargs['id'] = poi_id

        r = requests.get(f"https://api.tomtom.com/search/2/poiDetails.{ext}?{urllib.parse.urlencode(kwargs)}")
        r.raise_for_status()
        return json.loads(r.content)