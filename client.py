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

BUSINESS_PATH = 'http://www.yelp.com/biz/'
# Limit on number of businesses returned from the search
SEARCH_LIMIT = 10
# Limit on the number of biz-photo (photo box) images
PHOTO_LIMIT = 20

app = Flask(__name__)

IS_PRODUCTION = (os.getenv('PYTHON_ENV', False) == "production")
if not IS_PRODUCTION:
    app.debug = True

def is_match(str1, str2):
    return str1 in str2

@app.route('/googlemap/')
def googlemap():
    """ Home Page """
    return render_template('googlemap.html')


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

    url_for_geoloc = 'http://freegeoip.net/json/' + client_ip
    query_resp = requests.get(url_for_geoloc)
    geoloc_json = json.loads(query_resp.content)

    zipcode = geoloc_json['zip_code']
    city = geoloc_json['city']
    region = geoloc_json['region_name'] or geoloc_json['region_code']
    country = geoloc_json['country_name'] or geoloc_json['country_code']
    default_loc = 'San Francisco, CA'

    if city == "":
        loc = default_loc
    else:
        if region == "":
            loc = default_loc
        else:
            loc = ''.join([city, ', ', region , ', ', country]) 


    print "location is %s" %loc
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
    buss_obj = Businesses(response, 
                          BUSINESS_PATH,
                          PHOTO_BOX_PATH, 
                          SEARCH_LIMIT, 
                          PHOTO_LIMIT)

    ret_val = buss_obj.get_biz_photos(response)

    print str(time()-a)

    return ret_val

if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
