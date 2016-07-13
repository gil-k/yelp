# -*- coding: UTF-8 -*-
from flask import request               # to access url query string

import requests         # for http get/post calls
import json             # http query responses handled as json 

''' Yelp API query parameter strings '''
from yelp2.config import TERM           # search category of business
from yelp2.config import LOCATION       # city/state/country of business
from yelp2.config import LIMIT          #
from yelp2.config import SORT           # sorting criteria of search response, default is 0
                                        # 0
                                        # 1
                                        # 2

from yelp2.config import SEARCH_LIMIT       # maximum number of businesses displayed per page
from yelp2.config import DEFAULT_LOCATION   # default location for yelp search query
from yelp2.config import CREDENTIAL_FILE    # credential for Yelp API


class Url_Params(object):

    def __init__(self):
        # self.request_args = request_args
        self.url_params = {}#{LIMIT: SEARCH_LIMIT}


    def get_url_params(self):#, request_args):
        self.url_params.update({LIMIT: SEARCH_LIMIT})
        if TERM in request.args:
            term = request.args.get(TERM)
            self.url_params.update({TERM: term.replace(' ', '+')})

        if LOCATION in request.args:
            term = request.args.get(LOCATION)
            self.url_params.update({LOCATION: term.replace(' ', '+')})
        else:
            self.url_params.update({LOCATION: DEFAULT_LOCATION.replace(' ', '+')})

        if SORT in request.args:
            self.url_params.update({SORT: request.args.get(SORT)})

        return self.url_params



    def get_location(self, client_ip):
        # url for ip based geolocation query
        url_for_geoloc = 'http://freegeoip.net/json/' + client_ip

        # init location variable
        loc = ""

        try:
            # obtain ip based geolocation information
            query_resp = requests.get(url_for_geoloc, verify=False, timeout=3)
            # convert query response to json object
            geoloc_json = json.loads(query_resp.content)
        except requests.exceptions.RequestException as e:
            # if exception occurs or if times out after 3 seconds, default location used
            print "exception in url_params:get_location"
            return DEFAULT_LOCATION
        
        # parse city, state, country or zipcode from json query response
        zipcode = geoloc_json['zip_code'] or ""
        city = geoloc_json['city'] or ""
        region = geoloc_json['region_name'] or geoloc_json['region_code'] or ""
        country = geoloc_json['country_name'] or geoloc_json['country_code'] or ""
        
        # format location depending on which geolocation data are defined
        if city == "":
            loc = DEFAULT_LOCATION
        else:
            if region == "":
                loc = city
            else:
                if country == "":
                    loc = ''.join([city, ', ', region]) 
                else:
                    loc = ''.join([city, ', ', region , ', ', country]) 

        return loc
