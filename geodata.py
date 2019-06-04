import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from ratelimit import limits

geolocator = Nominatim(scheme="http")
URL_INIT = "https://twitter.com/"

arr = np.load('data_sent.npy')
labels = [
  'id', 'text_work', 'fullname', 'html', 'likes',
  'replies', 'retweets', 'text_raw', 'timestamp', 
  'url', 'user', 'sen'
  ]
df = pd.DataFrame(arr, columns=labels)

users = df['user'].unique()

ONE_SECOND = 1

@limits(calls=1, period=ONE_SECOND)
def get_location(users):

    loc = pd.DataFrame(columns=['user', 'latitude', 'longitude'])

    print("Querying location ...")
    print(f"Temps estimé : {(len(users)*2)/60} minutes or {(len(users)*2)/60/60} hours for {len(users)} users.")

    for i in range(len(users)):

        if i % 100 == 0:
            print(f"Querying from user {i} to {i+99}")

        html = requests.get(URL_INIT+users[i])
        soup = BeautifulSoup(html.text, "lxml")
        location = soup.find("span", {"class": "ProfileHeaderCard-locationText"}).text.strip()
        if location == "":
            pass
        else:
            try:
                adress = geolocator.geocode(location, timeout=50)
                if adress is not None:
                    loc = loc.append({
                        'user': users[i], 'latitude': adress.latitude, 'longitude': adress.longitude
                        }, ignore_index=True)
            except GeocoderTimedOut as e:
                print("Error: geocode failed on input %s with message %s"%(location, e))

    loc.to_csv('user_locations.csv')

get_location(users)

print("Le fichier .CSV contenant les coordonnées GPS a été créé avec succès !")