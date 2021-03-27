import herepy
import time 
import pprint
#import googlemaps # unused
from rich import print as print

places_api = herepy.PlacesApi(api_key='MBW86o6Sr5MNPA4d71hJ60BXa2hGNt3rxhYUVhqU5Ho')

places_result = places_api.places_in_circle(coordinates = ['42.053162', '-82.599884'], radius = 50000, query = 'farm', limit=20, lang='en-US').as_dict()

print(places_result)
