#!/usr/bin/python3

import json
import os
import requests

LAT = "39.753325"
LONG = "-105.003294"
CACHE_FILE = "restaurants.txt"
KEY = os.environ['ZOMATO_API_KEY']
REQUEST_URL="https://developers.zomato.com/api/v2.1/search\
?entity_id=305&lat=39.753325&lon=-105.003294&radius=1000\
&cuisines=1%2C3%2C148%2C55"
HEADERS={'user-key': KEY}

def get_restaurants():
    """
    Loads restaurants from the Zomato API
    """
    restaurants = []
    start = 0

    while(True):
        response = requests.get(REQUEST_URL + "&start=" + str(start), \
                                headers=HEADERS)
        response_body = json.loads(response.text)
        if (response_body["results_shown"] < 1):
            break
        
        restaurants += response_body["restaurants"]        
        start += 20

    return restaurants


def load_restaurants():
    """Tries to load restaurants
    If restaurants have been stored locally from a previous run, uses
    the stored files to avoid hitting the API. Otherwise, grabs
    restaurants from the API
    """
    try:
        with open(CACHE_FILE) as infile:
            print("Cache found, loading from file {}".format(CACHE_FILE))
            restaurants = json.load(infile)
    except Exception:
        print("No cache found, loading from API")
        restaurants = get_restaurants()
        with open(CACHE_FILE, 'w+') as outfile:
            json.dump(restaurants, outfile)
            return restaurants
    return restaurants

if __name__ == "__main__":
    restaurants = load_restaurants()
