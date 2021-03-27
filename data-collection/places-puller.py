import sqlite3
import herepy
import dotenv
import os
#from rich import print as print

dotenv.load_dotenv() # Load from .env

places_api = herepy.PlacesApi(api_key=os.getenv("HERE_API_KEY")) # Initialize api


coords = [ # Three places in the area to search near
    ["42.2813", "-82.29832"],
    ["42.15112", "-82.52628"],
    ["42.15417", "-82.89021"]
]

# Execute search
combined_results = []
for pair in coords:
    results = places_api.places_in_circle(pair, radius=15000, query = "farm", limit = 100)
    #print(len(results.as_dict()['items']))
    combined_results += results.as_dict()['items']

#print(len(combined_results))

# Filter duplicates
final_results = []
for x in combined_results:
    if not any(y['id'] == x['id'] for y in final_results): # Check for a result with the same entry already in the final list
        final_results.append(x)

#print(len(final_results))
#print(final_results)