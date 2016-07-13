# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, current_app, render_template, request

import os
import json             # http query responses handled as json 
                        # (in python requests/grequests and ajax calls)
import requests         # for http get/post calls

from time import time   # to measure elapsed time for debugging purpose


''' 'yelp' module for Yelp API '''
# from yelp.config import SEARCH_PATH     # search url per Yelp API
# from yelp.oauth1_authenticator import Oauth1Authenticator     # Yelp authentication
# from yelp.client import Client     # search ops performed via client obj


''' 'yelp2' module is my contribution for extracting photos '''
# (aka 'biz_photos') from businesses including helper classes
from yelp2.url_params import Url_Params     # set up parameters to use Yelp search API
# from yelp2.businesses import Businesses     # extracts business info and photos
# from yelp2.config import CREDENTIAL_FILE    # credential for Yelp API
# from yelp2.config import BUSINESS_PATH      # business page is ~ http://www.yelp.com/biz/"business-id"
# from yelp2.config import PHOTO_BOX_PATH     # url path for business's photos, aka biz-photos
# from yelp2.config import SEARCH_LIMIT       # maximum number of businesses displayed per page
# from yelp2.config import PHOTO_LIMIT        # maximum number of biz-photos displayed per row
# from yelp2.config import DEFAULT_TERM       # default term/category for yelp search query
from yelp2.config import DEFAULT_LOCATION   # default location for yelp search query
from yelp2.visual_client import Visual_Client

app = Flask(__name__)

IS_PRODUCTION = (os.getenv('PYTHON_ENV', False) == "production")
if not IS_PRODUCTION:
    app.debug = True




''' landing page for ATITAN.NET, personal page for Gil Kwak '''
@app.route('/')
def index():
    # displays following links:

    link_id_1 = 'Visual Yelp'       # "visual-yelp page"
    link_url_1 = '/yelp/'

    
    link_id_2 = 'LinkedIn Page'     # personal LinkedIn page"
    link_url_2 = 'https://www.linkedin.com/in/gilkwak'

    return render_template('index.html', 
                            link_id_1=link_id_1, 
                            link_url_1=link_url_1,
                            link_id_2=link_id_2, 
                            link_url_2=link_url_2)




''' "visual" presentation of yelp search '''
@app.route('/yelp/')
def yelp():
    # from businesses objects returned from '/yelp/?term=category&location=region'
    # query, extracts biz-photos from businesses' photo-box page, and displays the 
    # photos in a row per business, includes interactive google map.

    # term/category & location obtained from two input fields.
    # query results displayed in "search_results" div element

    # visitor first sees yelp results with default term/category and
    # ip-obtained geolocation or default location displayed on page

    # browser ip used for obtain geolocation
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # util functions to generate search query parameters
    util = Url_Params()

    # pass location info to yelp page
    return render_template('yelp.html', loc=util.get_location(client_ip))


    # # url for ip based geolocation query
    # url_for_geoloc = 'http://freegeoip.net/json/' + client_ip
    
    # # init location variable
    # loc = ""

    # try:
    #     # obtain ip based geolocation information
    #     query_resp = requests.get(url_for_geoloc, verify=False, timeout=3)
    #     # convert query response to json object
    #     geoloc_json = json.loads(query_resp.content)
    # except requests.exceptions.RequestException as e:
    #     # if exception occurs or if times out after 3 seconds, default location used
    #     print "exception-geolocation query"
    #     loc = DEFAULT_LOCATION
    
    # # if exception occurred use default location
    # if loc == DEFAULT_LOCATION:
    #     return render_template('yelp.html', loc=loc)
    


    # # parse city, state, country or zipcode from json query response
    # zipcode = geoloc_json['zip_code'] or ""
    # city = geoloc_json['city'] or ""
    # region = geoloc_json['region_name'] or geoloc_json['region_code'] or ""
    # country = geoloc_json['country_name'] or geoloc_json['country_code'] or ""
    
    # # format location depending on which geolocation data are defined
    # if city == "":
    #     loc = DEFAULT_LOCATION
    # else:
    #     if region == "":
    #         loc = city
    #     else:
    #         if country == "":
    #             loc = ''.join([city, ', ', region]) 
    #         else:
    #             loc = ''.join([city, ', ', region , ', ', country]) 

    # # pass location info to yelp page
    # return render_template('yelp.html', loc=loc)

    
""" Displays results of Yelp http get request """
@app.route("/search/", methods=["GET"])
def main():
    
    a = time()     # to measure elapsed time

    # client for yelp query request & process response for 
    # visual display of results (biz-photos for each businesses)
    client = Visual_Client()
    biz_photos = client.get_biz_photos()

    print str(time()-a)     # to measure elapsed time

    return biz_photos   # json containing html for biz-photos and
                        # longitudes and latitudes of businesses for google map


    # # Load YELP API credential file
    # with open(CREDENTIAL_FILE) as credential_json:
    #     credentials = json.load(credential_json)

    # Create credential object
    # auth = Oauth1Authenticator(**credentials)

    # Create client object with credentials
    # client = Client(auth)

    # # Parses input fields for Yelp search url parameters
    # param = Url_Params()

    # # Get list of businesses for chosen categories and region
    # response = client._make_request(SEARCH_PATH, param.get_url_params())#request.args))

    # # Obtain business info (name, rating, address, etc.) and
    # # urls for biz-photo (photo box) images for each businesses
    # buss_obj = Businesses(response, 
    #                       BUSINESS_PATH,
    #                       PHOTO_BOX_PATH, 
    #                       SEARCH_LIMIT, 
    #                       PHOTO_LIMIT)

    # ret_val = buss_obj.get_biz_photos(response)

    # print str(time()-a)

    # return ret_val


# test page for google map
@app.route('/googlemap/')
def googlemap():
    return render_template('googlemap.html')


# on-going test page
@app.route('/test2/')
def test():
    return render_template('test2.html')


if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
