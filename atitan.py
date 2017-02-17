# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, current_app, render_template, request

import os
import sys
import json             # http query responses handled as json 
                        # (in python requests/grequests and ajax calls)
import requests         # for http get/post calls
from time import time   # to measure elapsed time for debugging purpose


''' 'yelp2' module is my contribution for extracting photos (biz-photos) '''
from yelp2.url_params import Url_Params     # set up parameters to use Yelp search API
from yelp2.config import DEFAULT_TERM       # term/category for yelp search query in case term input field is empty
from yelp2.config import DEFAULT_LOCATION   # default location for yelp search query
from yelp2.visual_yelp import Visual_Yelp # wrapper for yelp client object
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)

IS_PRODUCTION = (os.getenv('PYTHON_ENV', False) == "production")
if not IS_PRODUCTION:
    app.debug = True


''' "visual" presentation of yelp search results '''
@app.route('/')
def yelp():
    # app.logger.warning('warning message')
    # app.logger.error('error message')
    #logging.basicConfig(filename='atitan.log', level=logging.WARNING)
    #logging.debug('debug message')
    #logging.info('info message')
    #logging.warning('warning message')
    # business photos (biz-photos) are extracted from yelp search results, 
    # and displayed one business per row. 

    # biz-photos are found on each business' photo-box page. Formatted results
    # are appended to "search-results" div tag in body.

    # Yelp query string is '/yelp/?term=category&location=region'
    # business term or category and location are taken from input fields

    # visitor first sees yelp results with default term/category and
    # ip-obtained geolocation displayed on page
    
    # browser ip used to obtain geolocation
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # util functions to generate search query parameters
    # in case of error default term/category & location values used
    util = Url_Params()
    location = util.get_location(client_ip)
    
    # pass location info to yelp page
    return render_template('yelp.html', term=DEFAULT_TERM, loc=location)


''' landing page for ATITAN.NET '''
@app.route('/kd')
def kd():
     return render_template('kd.html')

''' landing page for ATITAN.NET '''
@app.route('/home')
def index():
    #if hasattr(sys, 'real_prefix'):
    #    return render_template('index.html')
    #else:
    #    return "no virtual environment found"

     # displays following links:
     link_id_1 = 'YelpPhotos'       # "visual-yelp page"
     link_url_1 = '/yelp/'
     link_id_2 = 'LinkedIn'     # personal LinkedIn page"
     link_url_2 = 'https://www.linkedin.com/in/gilkwak'

     return render_template('index.html', 
                             link_id_1=link_id_1, 
                             link_url_1=link_url_1,
                             link_id_2=link_id_2, 
                             link_url_2=link_url_2)

    
""" Displays results of Yelp http get request """
@app.route("/search/", methods=["GET"])
def main():
    
    a = time()     # to measure elapsed time

    # decorator for Yelp client for search query & process response for 
    # visual display of results (biz-photos for each businesses)
    yelp = Visual_Yelp()
    biz_photos = yelp.biz_photos()

    # print str(time()-a)     # to measure elapsed time

    return biz_photos   # json containing status, html for biz-photos,
                        # longitudes and latitudes of businesses for google map

# test page for google map
@app.route('/googlemap/')
def googlemap():
    return render_template('googlemap.html')

# on-going test page
@app.route('/gumsa/')
def test():
    # browser ip used to obtain geolocation
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    util = Url_Params()
    location = util.get_location(client_ip) 

    # print "Location is %s." % location
    return render_template('yelp.html', term=DEFAULT_TERM, loc=location)
    # return render_template('test.html')


if __name__ == "__main__":
    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    if app.debug:
        app.run(
            host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', '8080'))
        )
    else:
        app.run()

