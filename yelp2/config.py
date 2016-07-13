# credential file for Yelp API
CREDENTIAL_FILE = 'static/config_secret.json'

# business page on yelp.com is at  http://www.yelp.com/biz/"business-id"
BUSINESS_PATH = 'http://www.yelp.com/biz/'

# url path for photos for a business, aka biz-photos, are at
# http://www.yelp.com/biz_photos/"business-id"
PHOTO_BOX_PATH = 'http://www.yelp.com/biz_photos/'

# maximum number of businesses displayed per page
# currently set to 9 total until google map marker label can display 
# more than 1 character
SEARCH_LIMIT = 9

# maximum number of biz-photos found in "photo-box" of a business
# displayed in a single row, on page
PHOTO_LIMIT = 20

# term/category for yelp search query in case term input field is empty
DEFAULT_TERM = 'dinner'

# location used in yelp search query in case location input field is empty
# or unable to obtain geolocation from ip during first page visit
DEFAULT_LOCATION = 'San Francisco, CA'

# YELP BUSINESS CATEGORY FOR SEARCH
TERM = 'term'

# YELP BUSINESS SEARCH LOCATION
LOCATION = 'location'

SORT = 'sort'

LIMIT = 'limit'

CRED_ERROR = '<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yelp API credential error, please retry.</h3>'

AUTH_ERROR = '<p><h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yelp API authentication error, please retry.</h3>'