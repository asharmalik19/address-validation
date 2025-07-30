import os

import requests
from dotenv import load_dotenv
import pandas as pd
from geopy.distance import geodesic

load_dotenv()
API_KEY = os.getenv('API_KEY')

def geocode(place) -> dict:
    geocode_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': place,
        'key': API_KEY
    }
    response = requests.get(geocode_api_url, params=params)
    response_json = response.json()
    geometry = response_json['results'][0]['geometry']['location']
    return geometry

def find_place(place, business_name) -> dict:
    """We assume that this function returns the correct place, i.e, the 
    business with the same or new address. It can sometimes match an incorrect
    business and that case is not handled here. Even if it matches a different
    business on the same address, it doesn't affect our use-case. We want to 
    capture the cases where a same business has different address in our file and
    on the map."""
    places_api_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': place,
        'inputtype': 'textquery',
        'fields': 'name,formatted_address',
        'key': API_KEY
    }
    response = requests.get(places_api_url, params=params)
    found_places = response.json()
    if len(found_places['candidates']) > 1:
        for place in found_places['candidates']:
            if place['name'].lower() == business_name.lower():
                return place
        return None
    if len(found_places['candidates']) == 0:
        return None
    if len(found_places['candidates']) == 1:
        return found_places['candidates'][0]

def is_coordinates_same(place_coordinates, found_place_coordinates) -> bool:
    """The coordinates return by geocoding api can sometimes differ
    by a small fraction. This function provides a flexible way to 
    compare the coordinates and checks if they are really different."""
    THRESHOLD = 50 # meters
    distance = geodesic(
        (place_coordinates['lat'], place_coordinates['lng']),
        (found_place_coordinates['lat'], found_place_coordinates['lng'])
    ).meters
    return distance <= THRESHOLD


if __name__ == '__main__':
    df = pd.read_csv('CALI DM List.csv').iloc[22:50]
    df['Matched Place'] = None

    for index, row in df.iterrows():
        bid = row['BID']
        business_name = row['Business Name']
        # place is the combination of business name and its address
        place = row['Full Address']

        found_place = find_place(place, business_name)
        if found_place is None:
            print(f'No place found for {place}')
            continue
        found_place_str = found_place['name'] + ' ' + found_place['formatted_address']
        place_coordinates = geocode(place)
        found_place_coordinates = geocode(found_place_str)

        if not is_coordinates_same(place_coordinates, found_place_coordinates):
            df.at[index, 'Matched Place'] = found_place_str
    
    df.to_csv('validated_addresses.csv', index=False)
            
            


        




        

            

        






