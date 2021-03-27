import sqlite3
import herepy
import dotenv
import os
#from rich import print as print

dotenv.load_dotenv()

places_api = herepy.PlacesApi(api_key=os.getenv("HERE_API_KEY"))

