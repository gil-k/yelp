# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, current_app, render_template, request

import os
import json
import requests
import re

# Measure runtime intervals, remove when no longer needed
from time import time

# Yelp's search url path
from yelp.config import SEARCH_PATH
# Yelp's API classes
from yelp.oauth1_authenticator import Oauth1Authenticator
from yelp.client import Client

# yelp2 contains my helper classes
# Extracts user's Yelp search url parameters
from yelp2.url_params import Url_Params
# Businesses object handles all biz photo (photo box) tasks
from yelp2.businesses import Businesses

# Credential for Yelp API
CREDENTIAL_FILE = 'static/config_secret.json'
# Url path for biz-photos (photo box) images
PHOTO_BOX_PATH = 'http://www.yelp.com/biz_photos/'
# Limit on number of businesses returned from the search
SEARCH_LIMIT = 10
# Limit on the number of biz-photo (photo box) images
PHOTO_LIMIT = 20

app = Flask(__name__)

IS_PRODUCTION = (os.getenv('PYTHON_ENV', False) == "production")
if not IS_PRODUCTION:
    app.debug = True

@app.route('/')
def index():
    """ Home Page """
    return render_template('index.html', page_id_1='Visual Yelp', page_url_1='/yelp/',
        page_id_2='LinkedIn', page_url_2='https://www.linkedin.com/in/gilkwak')


@app.route('/yelp/')
def yelp():
    """ Yelp 'visual' search page 
        uses '/yelp/?term=category&location=city, state' to make yelp search request
        displays results returned in div tag below the 'visual' search input fields
        and the search button
    """
    a = time()
    # get client ip address
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
 
    # client_ip = '199.47.217.97' #Dropbox, SF
    # client_ip = '147.126.10.148' # Chicago


    # trial key to get geolocation based on ip, from Eurekapi.com
    eurekapi_key = 'SAK54X6U927WR4TS7RWZ'

    # get geolocation data from Eurekapi.com
    response = requests.get('http://api.eurekapi.com/iplocation/v1.8/locateip?key=' + 
        eurekapi_key + '&ip=' + client_ip + '&format=JSON&compact=Y')

    # convert stringfied json to json object & extract desired details 
    # like 'Los Angeles, California, United States'
    data = json.loads(response.text)

    query_status = data['query_status']['query_status_code']

    # if invalid ip or loopback, use San Francisco as location
    if re.match(query_status, 'OK') is None:
        loc = 'San Francisco, CA'
    else:    
        geoloc = data['geolocation_data']
        city = geoloc['city']
        region_name = geoloc['region_name']
        country_name = geoloc['country_name']

        loc = ''.join([city + ', ' + region_name + ', ' + country_name])
    
    print str(time()-a)
    # show yelp.html and pass the location data
    return render_template('yelp.html', loc=loc)

    
""" Displays results of Yelp http get request """
@app.route("/search/", methods=["GET"])
def main():

    a = time()

    # Load credential file
    with open(CREDENTIAL_FILE) as credential_json:
        credentials = json.load(credential_json)

    # Create credential object
    auth = Oauth1Authenticator(**credentials)

    # Create client object with credentials
    client = Client(auth)

    # Parses input fields for Yelp search url parameters
    url_param_obj = Url_Params(request.args, SEARCH_LIMIT)

    # Get list of businesses for chosen categories and region
    response = client._make_request(SEARCH_PATH, url_param_obj.get_url_params())

    # Obtain business info (name, rating, address, etc.) and
    # urls for biz-photo (photo box) images for each businesses
    buss_obj = Businesses(response, PHOTO_BOX_PATH, SEARCH_LIMIT, PHOTO_LIMIT)

    ret_val = buss_obj.get_biz_photos(response)

    print str(time()-a)

    return ret_val

if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
