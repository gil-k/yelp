# -*- coding: UTF-8 -*-

from HTMLParser import HTMLParser

# from yelp2.config2 import PHOTO_LIMIT

class Parser(HTMLParser):

    def __init__(self, photo_limit):
        HTMLParser.__init__(self)
        self.photo_limit = photo_limit
        self.attrs_count = 0
        self.data = []
        self.src = ""
        self.business_photo_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.attrs_count = 0

            for name, value in attrs:
                if name == 'class' and value == 'photo-box-img':
                    self.attrs_count += 1
                    #print ''.join([name, " found ", str(self.attrs_count)])
                if name == 'height' and value == '226':
                    self.attrs_count += 1
                    #print ''.join([name, " found ", str(self.attrs_count)])
                if name == 'src':
                    self.src = value

            if self.business_photo_count < self.photo_limit and self.attrs_count == 2:
                self.data.append(''.join(["<img src='https:", 
                                          self.src, 
                                          "' width='226' height='226' />",
                                          "&nbsp;"]))
                self.business_photo_count += 1
 