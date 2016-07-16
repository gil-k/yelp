# -*- coding: UTF-8 -*-
import grequests
import json

'''  'yelp2' module is my contribution for extracting photos (biz-photos) '''

# Given business 'id', parser scrapes photo-box page of each businesses, and
# extracts 226x226 biz-photos in 'photo-box-img' tags, to be displayed
# on a row per business.  Significantly faster than Beautiful Soup, etc.
from yelp2.parser import Parser

from yelp2.config import BUSINESS_PATH      # business page is ~ http://www.yelp.com/biz/"business-id"
from yelp2.config import PHOTO_BOX_PATH     # url path for business's photos, aka biz-photos
from yelp2.config import SEARCH_LIMIT       # maximum number of businesses displayed per page
from yelp2.config import PHOTO_LIMIT        # maximum number of biz-photos displayed per row
from yelp2.config import PIC_FILTER        # filter for biz_photos

# Decorator for businesses json from Yelp search response 
class Businesses(object):

    def __init__(self, response):
        # query response from Yelp search
        self.response = response
        # list of businesses from query response
        self.businesses = {}
        # list of photo-box urls containing biz-photos for businesses
        self.photo_box_urls = []
        # list of business info (name, rating, address, etc.) and biz-photos
        self.html = []
        # latitude & longitude coordinate of businesses
        self.lng = []
        self.lat = []

    # returns business info (name, rating, address, etc.) and biz-photo images
    # displayed per row per business, up to self.photo_limit images per business
    def get_biz_photos(self):
        # get list of businesses from Yelp query response
        try:
            self.businesses = self.response.get('businesses')
        except Exception, e:
            raise

        # get urls for photo-box pages of businesses in order to extract biz-photos
        try:
            self.get_photo_urls();
        except Exception, e:
            raise

        # retrieve phot-box pages of all the businesses, using non-blocking call
        try:
            unsent_request = (grequests.get(url) for url in self.photo_box_urls)
            photo_box_responses = grequests.map(unsent_request) 
        except Exception, e:
            raise

        # get latitudes and longitudes of businesses, center is average of coordinates
        try:
            self.get_coordinates();
        except Exception, e:
            raise

        # scrap biz-photos from photo-box pages        
        try:
            rank = self.get_html(photo_box_responses);
        except Exception, e:
            raise

        # construct response json
        ret_val = { u"status": 'ok',
                    u"html": ''.join(self.html),
                    u"coords": rank+1,
                    u"lats": self.lat,
                    u"lngs": self.lng}
        try:
            return json.dumps(ret_val)
        except Exception, e:
            raise

    def get_photo_urls(self):
        # get biz-photos of businesses up to SEARCH_LIMIT businesses
        for rank in range(min(SEARCH_LIMIT, len(self.businesses))):
            business = self.businesses[rank]
            if business:
                self.photo_box_urls.append(''.join([PHOTO_BOX_PATH, 
                                                    business['id'],
                                                    PIC_FILTER]))       

    # get latitudes and longitudes of businesses, center is average of coordinates
    def get_coordinates(self):
        min_lat = 90;
        max_lat = -90;
        min_lng = 180;
        max_lng = -180;

        for rank in range(min(SEARCH_LIMIT, len(self.businesses))):
            business = self.businesses[rank]
            if business:
                if 'location' in business:
                    location = business['location']
                    if 'coordinate' in location:
                        coord = location['coordinate']
                        if 'latitude' in coord and 'longitude' in coord:
                            latitude = coord['latitude']
                            longitude = coord['longitude']
                            self.lat.append(latitude)
                            self.lng.append(longitude)
                            if latitude < min_lat:
                                min_lat = latitude
                            if latitude > max_lat:
                                max_lat = latitude
                            if longitude < min_lng:
                                min_lng = longitude
                            if longitude > max_lng:
                                max_lng = longitude
        
        if rank >= 0:
            avg_lat = (min_lat + max_lat) / 2
            avg_lng = (min_lng + max_lng) / 2
            self.lat.append(avg_lat)
            self.lng.append(avg_lng)

    def get_html(self, photo_box_responses):
        for rank in range(min(len(photo_box_responses), len(self.businesses))):
            business = self.businesses[rank]
            if business:
                try:
                    info = self.get_buss_info(business)
                except Exception, e:
                    raise

                self.html.append(''.join(["<div id=buss_container>", 
                                          "<span id='buss_info'>", 
                                          "&nbsp;&nbsp;<b>", 
                                          str(rank+1), 
                                          ".</b>&nbsp;",
                                          info, 
                                          "</span>"]))
                try:
                    biz_photos = self.parse_photo_box_images(photo_box_responses[rank], 
                                                             PHOTO_LIMIT)
                except Exception, e:
                    raise

                self.html.append(''.join(["<span>",#" class='photo_box'",#" id='row is ",
                                          # str(rank),
                                          # "' ",
                                          biz_photos,
                                          # "</span>"]))
                                          "</span></div>"]))
        # return total count businesses
        return rank

    def get_buss_info(self, business):
        name = ''
        rating  = ''
        reviews = ''
        address = ''
        phone = ''

        link_start = ''.join(["<a href='", 
                              BUSINESS_PATH,
                              business['id'],
                              # "'target='_blank'>"])
                              " 'class='business_link' target='_blank' >" ])
        link_end = "</a>"

        if 'name' in business:
            name = ''.join(["<b>", 
                            business['name'], 
                            "</b>"])

        if 'rating_img_url_large' in business:
            # smaller image business['rating_img_url_small']
            rating  = ''.join(["<img class='rating_img' src=' ", 
                               business['rating_img_url_large'],
                               # "' width='83' height='15'/>"])
                               # "' width='111' height='20'/>"])
                               "' width='166' height='30'/>"]) # native size

        # review count
        # reviews  = ''.join([" (", str(business['review_count']), " reviews) "])
        if 'review_count' in business:
            reviews  = ''.join([str(business['review_count']),
                                "&nbsp;&nbsp;reviews"])

        if 'location' in business:
            location = business['location']
            if 'address' in location:
                str_address = ''.join(location['address'])
            if 'city' in location:
                city = location['city']

            address = ''.join([",&nbsp;&nbsp;",
                               str_address,
                               ",&nbsp;&nbsp;",
                               city])

        if 'display_phone' in business:
            phone = ''.join([",&nbsp;&nbsp;",
                             business['display_phone']])

        # return ''.join([name, rating, reviews, address])
        return ''.join(["&nbsp;", link_start, name, link_end, 
                        "&nbsp;&nbsp;", 
                        link_start, rating, link_end, 
                        "&nbsp;&nbsp;", 
                        link_start, reviews, address, phone, link_end])

    # if insufficient biz-photos, fill with place holder images to fill a row
    def add_placeholder(self, html):
        # last two chars in html is number of biz photos
        biz_photos = int(html[-2:])
        new_html = []
        # remove last two chars from biz photo html
        new_html.append(html[:-2])
        
        # not enough biz-photos to fill a row, need PHOTO_LIMIT images
        if biz_photos < PHOTO_LIMIT:
            placeholder_img = "<img src='/static/yelp_images/placeholder.jpg' width='226' height='226'/>&nbsp;"

            for rank in range(PHOTO_LIMIT - biz_photos):
                new_html.append(placeholder_img)

        return ''.join(new_html)

    # scraps biz-photos from photo-box pages of each business
    def parse_photo_box_images(self, business_response, photo_limit):
        parser = Parser(PHOTO_LIMIT)
        try:
            parser.feed(business_response.content.decode('utf-8'))
            html = ''.join(parser.data)
        except Exception, e:
            raise
        finally:
            parser.close()

        # pad empty row with place holder
        try:
            return self.add_placeholder(html)
        except Exception, e:
            raise

