# -*- coding: UTF-8 -*-

# YELP BUSINESS CATEGORY FOR SEARCH
TERM = 'term'

# YELP BUSINESS SEARCH LOCATION
LOCATION = 'location'

SORT = 'sort'

# DEFAULT BUSINESS LOCATION
DEFAULT_LOCATION = 'San Francisco, CA'

LIMIT = 'limit'

class Url_Params(object):

    def __init__(self, request_args, search_limit):
        self.request_args = request_args
        self.url_params = {LIMIT: search_limit}

    def get_url_params(self):
        if TERM in self.request_args:
            term = self.request_args.get(TERM)
            self.url_params.update({TERM: term.replace(' ', '+')})

        if LOCATION in self.request_args:
            term = self.request_args.get(LOCATION)
            self.url_params.update({LOCATION: term.replace(' ', '+')})
        else:
            self.url_params.update({LOCATION: DEFAULT_LOCATION.replace(' ', '+')})

        if SORT in self.request_args:
            self.url_params.update({SORT: self.request_args.get(SORT)})

        return self.url_params
