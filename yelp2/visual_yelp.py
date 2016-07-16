# -*- coding: UTF-8 -*-

import json

'''  'yelp' module for Yelp API '''
from yelp.oauth1_authenticator import Oauth1Authenticator     # for Yelp search API 
from yelp.client import Client     	    # search ops performed via client obj
from yelp.config import SEARCH_PATH     # search url per Yelp API


'''  'yelp2' module is my contribution for extracting photos (biz-photos) '''
from yelp2.businesses import Businesses     # extracts business info and photos
from yelp2.url_params import Url_Params     # set up parameters to use Yelp search API
from yelp2.config import CREDENTIAL_FILE    # credential for Yelp API
from yelp2.config import CRED_ERROR         # error message for yelp credential error
from yelp2.config import AUTH_ERROR         # error message for yelp authentication error
from yelp2.config import PARAM_ERROR        # error message for input fields
from yelp2.config import YELP_ERROR        # error message for input fields
from yelp2.config import PARSE_ERROR        # error message for input fields


class Visual_Yelp(object):

    def __init__(self):
        self.credentials = {}
        
    # load Yelp API credential json file
    def get_credentials(self):
        try:
            with open(CREDENTIAL_FILE) as credential_json:
                credentials = json.load(credential_json)
        except Exception, e:
            credentials = None
        finally:
            return credentials


    # Yelp client object with credentials
    def get_client(self):
        try:
            # credential object
            auth = Oauth1Authenticator(**self.credentials)
            # client object with credentials
            client = Client(auth)
        except Exception, e:
            client = None
        finally:
            return client


    def biz_photos(self):
        # load Yelp API credential json file
        self.credentials = self.get_credentials()
        if self.credentials == None:
            return self.set_response_json('error', CRED_ERROR)

        # Yelp client object with credentials
        client = self.get_client()
        if client == None:
            return self.set_response_json('error', AUTH_ERROR)

        # parse url for search terms, location [& sorting method]
        param = Url_Params()
        url_params = param.get_url_params()
        if url_params == None:
            return self.set_response_json('error', PARAM_ERROR)

        # Get list of businesses for chosen categories and region
        try:
            response = client._make_request(SEARCH_PATH, url_params)
        except Exception, e:
            return self.set_response_json('error', YELP_ERROR) 


        # decorator for businesses results from Yelp search
        buss_obj = Businesses(response)
        try:
            # from search response, get business infos, and
            # get biz-photos from photo box page of each businesses
            biz_photos = buss_obj.get_biz_photos()
        except Exception, e:
            biz_photos = self.set_response_json('error', PARSE_ERROR) 
        finally:
            return biz_photos


    # response from query results or error to be passed to yelp.html
    def set_response_json(self, status, html, coords=None, lats=None, lngs=None):
        response = {u'status': status, u'html': html}
        # no of businesses in query results
        if coords:
            response.update({u'coords': coords})
        # list of latitudes of businesses
        if lats:
            response.update({u'lats': lats})
        # list of latitudes of businesses
        if lngs:
            response.update({u'lngs': lngs})
        # average of lats & lngs, center of all businesses, is in lats[coords], etc.

        return json.dumps(response)
