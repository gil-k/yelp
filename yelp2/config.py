''' paths for Yelp business pages and biz-photos pages '''
# credential file for Yelp API
CREDENTIAL_FILE = 'static/config_secret.json'
# business page on yelp.com is at  http://www.yelp.com/biz/"business-id"
BUSINESS_PATH = 'http://www.yelp.com/biz/'
# url path for photos for a business, aka biz-photos, are at
# http://www.yelp.com/biz_photos/"business-id"
PHOTO_BOX_PATH = 'http://www.yelp.com/biz_photos/'


''' default values for displaying Yelp search results visually '''
# maximum number of businesses displayed per page
# currently set to 9 total until google map marker label can display 
# more than 1 character
SEARCH_LIMIT = 10
# maximum number of biz-photos found in "photo-box" of a business
# displayed in a single row, on page
PHOTO_LIMIT = 10
# term/category for yelp search query in case term input field is empty
DEFAULT_TERM = 'dinner'
# location used in yelp search query in case location input field is empty
# or unable to obtain geolocation from ip during first page visit
DEFAULT_LOCATION = 'San Francisco, CA'
# sorting method of results, 0=default, 1=distance, 2=highest rated
DEFAULT_SORT = 0

# filter for biz-photos: all, food, inside, utside, menu or drink
PIC_FILTER = ''#?tab=drink'

''' url query terms for Yelp API '''
TERM = 'term'				# category of businesses
LOCATION = 'location'		# location of businesses
SORT = 'sort'				# sorting method for query response
LIMIT = 'limit'				# maximum business listings returned


''' error messages '''
# error loading Yelp credential file
CRED_ERROR = '<p><h3>&nbsp;&nbsp;Unable to load Yelp credential file.  Please retry.</h3>'
# error creating authenticated Yelp client object, from yelp.client module
AUTH_ERROR = '<p><h3>&nbsp;&nbsp;Yelp authentication error occurred, please retry.</h3>'
# error validating url query parameters using request.args
PARAM_ERROR = '<p><h3>&nbsp;&nbsp;Please check your search category & location, and retry.</h3>'
# invalid yelp query response
YELP_ERROR = '<p><h3>&nbsp;&nbsp;Oops! Unable to retrieve search results, please retry.</h3>'

PARSE_ERROR = '<p><h3>&nbsp;&nbsp;Oops! Unable to process search results, please retry.</h3>'
