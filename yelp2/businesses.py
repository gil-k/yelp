# -*- coding: UTF-8 -*-
import grequests
import json

# Extracts biz-photos (photo box) images which are 226x226 in elements with
# class name of 'photo-box-img'
from yelp2.parser import Parser

PIC_FILTER = '?tab=food'

class Businesses(object):

    def __init__(self, 
                 response, 
                 business_path,
                 photo_box_path, 
                 search_limit, 
                 photo_limit):
        # Response from Yelp search
        self.response = response
        self.business_path = business_path
        # Url for photo box images for each businesses
        self.photo_box_path = photo_box_path
        # Limit on number of businesses returned from the search
        self.search_limit = search_limit
        # Limit on the number of biz-photo (photo box) images
        self.photo_limit = photo_limit
        # List of businesses returned from Yelp search
        self.businesses = {}
        # List of urls for photo box images for each businesses
        self.photo_urls = []
        # List of business info & photo box images to be displayed
        self.html = []
        # Latitude & longitude coordinate of businesses
        self.lng = []
        self.lat = []


    # Return business info (name, rating, address, etc.) and phot box images,
    # up to self.photo_limit, for each business returned from Yelp search
    # def get_biz_photos0(self, response):
    #     self.businesses = response.get('businesses')

    #     for rank in range(min(self.search_limit, len(self.businesses))):
    #         business = self.businesses[rank]
    #         print business['id']
    #         if business:
    #             self.photo_urls.append(''.join([self.photo_box_path, business['id']]))

    #     unsent_request = (grequests.get(url) for url in self.photo_urls)
    #     biz_photo_responses = grequests.map(unsent_request) 

    #     self.html.append("<table style='background-color:#ffffcc' style='white-space:nowrap' cellpadding='5'>")

    #     for rank in range(min(len(biz_photo_responses), len(self.businesses))):
    #         business = self.businesses[rank]
    #         if business:
    #             self.html.append(''.join(["<tr><td>", 
    #                                       self.get_buss_info(business), 
    #                                       "</td></tr>"]))
    #             self.html.append(''.join(["<tr><td id='photo_box_images'>",
    #                                       self.parse_photo_box_images(biz_photo_responses[rank], self.photo_limit),
    #                                       "</td></tr>"]))

    #     self.html.append("</table>")
    #     return ''.join(self.html)

    # Return business info (name, rating, address, etc.) and phot box images,
    # up to self.photo_limit, for each business returned from Yelp search
    def get_biz_photos(self, response):
        self.businesses = response.get('businesses')

        for rank in range(min(self.search_limit, len(self.businesses))):
            business = self.businesses[rank]
            #print business['id']
            if business:
                self.photo_urls.append(''.join([self.photo_box_path, 
                                                business['id'],
                                                PIC_FILTER]))

        unsent_request = (grequests.get(url) for url in self.photo_urls)
        biz_photo_responses = grequests.map(unsent_request) 

        # self.html.append("<table style='background-color:#ffffcc' cellpadding='5'>")
        min_lat = 90;
        max_lat = -90;
        min_lng = 180;
        max_lng = -180;

        for rank in range(min(len(biz_photo_responses), len(self.businesses))):
            business = self.businesses[rank]
            if business:
                coord = business['location']['coordinate']
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

                # self.html.append(''.join(["<div id='business_info'>", 
                #                           self.get_buss_info(business), 
                #                           "</div>"]))
                # self.html.append(''.join(["<div id='photo_box'>",
                #                           self.parse_photo_box_images(biz_photo_responses[rank], 
                #                           self.photo_limit),
                #                           "</div>"]))
                self.html.append(''.join(["<div id=buss_container>", 
                                          "<span id='buss_info' class='outline'>", 
                                          "&nbsp;<font size='3'><b>", str(rank+1), ".</b></font>&nbsp;",
                                          self.get_buss_info(business), 
                                          "</span>"
                                          ]))
                self.html.append(''.join(["<span class='photo_box' id='row is ",
                                          str(rank),
                                          "' ",
                                          self.parse_photo_box_images(biz_photo_responses[rank], 
                                          self.photo_limit, rank),
                                          "</span>",
                                          "</div>"]))

                # self.html.append(''.join(["<div id=business_container>", 
                #                           "<div id='business_info'>", 
                #                           self.get_buss_info(business), 
                #                           "</div>"
                #                           ]))
                # self.html.append(''.join(["<div id='photo_box'>",
                #                           self.parse_photo_box_images(biz_photo_responses[rank], 
                #                           self.photo_limit),
                #                           "</div>",
                #                           "</div>"]))

        # self.html.append("</table>")
        avg_lat = (min_lat + max_lat) / 2
        avg_lng = (min_lng + max_lng) / 2
        self.lat.append(avg_lat)
        self.lng.append(avg_lng)

        ret_val = {u"status": 'ok',
                    u"html": ''.join(self.html),
                   u"coords": rank+1,
                   u"lats": self.lat,
                   u"lngs": self.lng}
        # return (''.join(self.html), self.latitude, self.longitude)
        # return ''.join(self.html)
        return json.dumps(ret_val)

    def get_buss_info(self, business):
        link_start = ''.join(["<a href='", 
                              self.business_path,
                              business['id'],
                              "' id='business_link' target='_blank'" ])

        name = ''.join(["&nbsp;<font size='3' color='696969'><b>", 
                        business['name'], "</b>"])
        # address = ', '.join(business['location']['display_address'])

        #rating  = ''.join(["<img src='", business['rating_img_url_large'],"' class='rotate270'/>"])
        # rating  = ''.join(["<img src='", business['rating_img_url_large'], "' width='133' height='24'/>"])
        # rating  = ''.join(["&nbsp;&nbsp;&nbsp;<img src='", business['rating_img_url_large'], "' width='66' height='12'/>"])
        rating  = ''.join(["<img src='", 
                           business['rating_img_url_large'], 
                           "' width='83' height='15'/>"])
        # rating  = ''.join(["&nbsp;<img src='", business['rating_img_url_small'], "'/>"])
        #rating  = ''.join(["<img src='", business['rating_img_url_large'], "' />"])

        # reviews  = ''.join([" (", str(business['review_count']), " reviews) "])
        reviews  = ''.join(["",
                            str(business['review_count']),
                            "&nbsp;reviews,&nbsp;"])


        str_address = ''.join(business['location']['address'])

        address = ''.join(["&nbsp;",
                            str_address,
                            ",&nbsp;&nbsp;",
                            business['location']['city'],
                            "</font>"])

                            # ", ", 
                            # loc['neighborhoods'], 
                            # ", ", 
                            # loc['city']
                            # ])
        link_end = "</a>"

        # return ''.join([name, rating, reviews, address])
        return ''.join([link_start, name, rating, reviews, address, link_end])

        # return ''.join([rating, 
        #                 "&nbsp; <font size='4' color='#666666'>", 
        #                 business['name'], 
        #                 "</font>",
        #                 " <font color='#666666'>", 
        #                 reviews, address, 
        #                 "</font>"])

        # return ''.join([rating, 
        #                 "&nbsp; <font color='#666666'><b>", business['name'], "</b></font>",
        #                 " <font color='#666666'>", reviews, address, "</font>"])

    def parse_photo_box_images(self, business_response, photo_limit, rank):
        parser = Parser(self.photo_limit, rank)
        parser.feed(business_response.content.decode('utf-8'))
        html = ''.join(parser.data)
        parser.close()
        return html

