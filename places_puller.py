
# This program has a function that will be executed once daily to update the data which gets sent to the frontend.

import tomtomutil as tt
import dotenv
import os
try:
    import ujson as json
except:
    import json
import datetime

# Import for debugging
#from rich import print

# Load from .env
dotenv.load_dotenv()

NOT_FOUND = "Not found"

def main():
    print("Downloading data...")
    
    # Initialize TomTom API
    TomTom = tt.TomTom(os.getenv("TOMTOM_API_KEY"))

    # Search for agricultural businesses in the area
    data = TomTom.fuzzySearch("", countrySet="CA", lat=42.15112, lon=-82.52628, topLeft="42.48172,-83.12779", btmRight="41.94877,-81.9344", categorySet="7335,7332004", limit=10000)

    # Record time
    data['summary']['timestamp'] = datetime.datetime.timestamp(datetime.datetime.now())


    for x in data['results']:
        
        # Combine with more details
        # Not all results will have metadata
        if "dataSources" in x.keys():
            poi_id = x['dataSources']['poiDetails'][0]['id']
            x['details'] = TomTom.detailSearch(poi_id)['result']

        # Descriptions
        try:
            desc = x['details']['description']
        except KeyError:
            category = x['poi']['categories'][0].lower()
            if category == "agriculture":
                category = "agriculture business"

            a_or_an = "a"
            if any(vowel in category for vowel in ['a', 'e', 'i', 'o', 'u']):
                a_or_an = "an"

            desc = f"{x['poi']['name']} is {a_or_an} {category} in {x['address']['localName']}."
        x['description'] = desc
        
        # Strip unnecessary data
        x['address'] = x['address']['freeformAddress']

        removable_fields = ['viewport', 'entryPoints', 'dataSources', 'info', 'id', 'dist', 'score', 'type']
        for f in removable_fields:
            if f in x.keys():
                x.pop(f)

        # Handle info under "poi"
        fields = ['name', 'phone', 'url', 'categories']
        for f in fields:
            if f in x['poi'].keys() and x['poi'][f]:
                x[f] = x['poi'][f]
            else:
                x[f] = NOT_FOUND

        # No longer needed
        x.pop('poi')

    # Save to JSON file
    json.dump(data, open("data.json", "w"))
    return data
