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
        self.url_params = {LIMIT: SEARCH_LIMIT}
        self.loc = ''

    def get_url_params(self):
        # if term/category & location query strings not in url, return None
        try:
            if TERM not in request.args or LOCATION not in request.args:
                return None;
            term = (request.args.get(TERM)).strip()
            if not term:
                return None;
            location = (request.args.get(LOCATION)).strip()
            if not location:
                return None;
        except Exception, e:
            return None;

        # append term/category query string to parameter dict
        self.url_params.update({TERM: term.replace(' ', '+')})
        self.url_params.update({LOCATION: location.replace(' ', '+')})

        # parse optional sort query string from url
        try:
            if SORT in request.args:
                sort = (request.args.get(SORT)).strip()
                if sort:
                    self.url_params.update({SORT: request.args.get(SORT)})
        except Exception, e:
            self.url_params = None
        finally:
            return self.url_params

    def get_location(self, client_ip):
        # url for ip based geolocation query
        url_for_geoloc = 'http://freegeoip.net/json/' + client_ip

        # obtain ip based geolocation information
        try:
            query_resp = requests.get(url_for_geoloc, verify=False, timeout=3)
            # convert query response to json object
            geoloc_json = json.loads(query_resp.content)
        except Exception, e:
            # if exception occurs or if times out after 3 seconds, default location used
            return DEFAULT_LOCATION
        
        # parse city, state, country or zipcode from json query response
        try:
            zipcode = geoloc_json['zip_code'] or ""
            city = geoloc_json['city'] or ""
            region = geoloc_json['region_name'] or geoloc_json['region_code'] or ""
            country = geoloc_json['country_name'] or geoloc_json['country_code'] or ""
        except Exception, e:
            return DEFAULT_LOCATION

        # format location depending on which geolocation data are defined
        if city == "":
            self.loc = DEFAULT_LOCATION
        else:
            if region == "":
                self.loc = city
            else:
                if country == "":
                    self.loc = ''.join([city, ', ', region]) 
                else:
                    self.loc = ''.join([city, ', ', region , ', ', country]) 
        return self.loc
