# -*- coding: UTF-8 -*-

import json

''' 'yelp' module for Yelp API '''
from yelp.oauth1_authenticator import Oauth1Authenticator     # for Yelp search API 
from yelp.client import Client     		# search ops performed via client obj
from yelp.config import SEARCH_PATH     # search url per Yelp API


''' 'yelp2' module is my contribution for extracting photos '''
from yelp2.businesses import Businesses     # extracts business info and photos
from yelp2.url_params import Url_Params     # set up parameters to use Yelp search API
from yelp2.config import BUSINESS_PATH      # business page is ~ http://www.yelp.com/biz/"business-id"
from yelp2.config import CREDENTIAL_FILE    # credential for Yelp API
from yelp2.config import PHOTO_BOX_PATH     # url path for business's photos, aka biz-photos
from yelp2.config import SEARCH_LIMIT       # maximum number of businesses displayed per page
from yelp2.config import PHOTO_LIMIT        # maximum number of biz-photos displayed per row
from yelp2.config import AUTH_ERROR	# error message for yelp authentication

class Visual_Client(object):

    def __init__(self):
        self.credentials = {}
        

    def get_credentials(self):
        # with open(self.credential_file) as credential_json:
        #     self.credentials = json.load(credential_json)
        try:
            with open(CREDENTIAL_FILE) as credential_json:
                self.credentials = json.load(credential_json)
        except Exception, e:
            return None

        return self.credentials


    def get_biz_photos(self):
    	# get Yelp API credential
        self.credentials = self.get_credentials()
        if self.credentials is None:
        	return self.get_response_json('fail', CRED_ERROR, '', '', '')

		# Create credential object
        auth = Oauth1Authenticator(**self.credentials)
        
        # Create client object with credentials
        client = Client(auth)

        # Parses input fields for Yelp search url parameters
        param = Url_Params()

        # Get list of businesses for chosen categories and region
        response = client._make_request(SEARCH_PATH, param.get_url_params())

	    # Obtain business info (name, rating, address, etc.) and
	    # urls for biz-photo (photo box) images for each businesses
        buss_obj = Businesses(response, 
                              BUSINESS_PATH,
                              PHOTO_BOX_PATH, 
                              SEARCH_LIMIT, 
                              PHOTO_LIMIT)
        return buss_obj.get_biz_photos(response)


    def get_response_json(self, status, html, coords, lats, lngs):
    	response = {u'status': status, 
    				u'html': html,
    				u'coords': coords,
    				u'lats': lats,
    				u'lngs': lngs}
        return json.dumps(response)






