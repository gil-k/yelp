# -*- coding: UTF-8 -*-
import logging

from HTMLParser import HTMLParser

#from yelp2.config2 import PHOTO_LIMIT

class Parser(HTMLParser):

    def __init__(self, photo_limit):
        HTMLParser.__init__(self)
        self.photo_limit = photo_limit
        self.attrs_count = 0
        self.data = []
        self.business_photo_count = 0

    def handle_starttag(self, tag, attrs):
        # parse only img tags
        if tag == 'img':
            self.attrs_count = 0

            # desired biz-photos are 226x226 and is photo-box-img class.
            # if self.attrs_count is 2, then img tag contains a biz-photo
            for name, value in attrs:
                if name == 'class' and value == 'photo-box-img':
                    self.attrs_count += 1
                    #print ''.join([name, " found ", str(self.attrs_count)])
                if name == 'height' and value == '226':
                    self.attrs_count += 1
                    #print ''.join([name, " found ", str(self.attrs_count)])
                if name == 'src':
                    # self.data.append(''.join(["<p>&nbsp;&nbsp;", value , "<p>",]))
                    src = value

            # append found biz-photo into parse data
            if self.business_photo_count < self.photo_limit and self.attrs_count == 2:
                # logging.basicConfig(filename='example.log', level=logging.DEBUG)
                # logging.debug(src)

                self.data.append(''.join(["&nbsp;<img src='",
               # self.data.append(''.join(["&nbsp;<img src='https:", 
                                          src, 
                                          "' width='226' height='226'/>"]))
                # self.data.append(''.join(["<p><p>&nbsp;&nbsp;",
                #                           src, 
                #                           "<p>"]))
                self.business_photo_count += 1

    def handle_endtag(self, tag):
        # append biz-photo count at end of html to return
        if tag == 'body':
            if self.business_photo_count < 10:
                img_count = '0' + str(self.business_photo_count)
            else:
                img_count = str(self.business_photo_count)

            self.data.append(''.join(["&nbsp;", img_count]))
 
