#!/usr/bin/env python
# encoding: utf-8
"""
gpx2epub.py

Created by Frank Rosquin on 2009-08-28.
Copyright (c) 2009 frank.rosquin.net. All rights reserved.
"""

import sys
import os
import re
import time
import argparse

from xml.dom import minidom

# import lxml.html
from lxml.html.clean import Cleaner, clean_html
import lxml.html.defs

# import pprint

class GPX:
    def __init__(self):
        self.cache_list     = []
        self.cache_source   = ""
        self.cache_data     = []
    
    def extract(self, ):
        """docstring for extract"""
        if re.search('\.gpx$', self.cache_source):
            self._extract_gpx(self.cache_source)
        else:
            for filename in os.listdir(self.cache_source):
                self._extract_gpx(self.cache_source + filename)
    
    def _extract_gpx(self, filename):
        """docstring for _extract_gpx"""    
        if not re.search('\.gpx$', filename):
            return
        gpx = self._load_gpx(filename)
        info = self._build_info(gpx)
        # name = os.path.basename(filename).split('.')[0]
        self.cache_data.append(info)
        # return info
        
    def _load_gpx(self, gpx_file):
        # print 'Parsing gpx file ' + os.path.basename(gpx_file)
        data = minidom.parse(gpx_file).documentElement
        data.normalize
        return data
    #
    def _build_info(self, gpx_data):
        info = {}
        info['name']    = gpx_data.getElementsByTagName('name')[1].firstChild.nodeValue
        info['lat']     = gpx_data.getElementsByTagName('wpt')[0].attributes['lat'].value
        info['lon']     = gpx_data.getElementsByTagName('wpt')[0].attributes['lon'].value
        info['type']    = gpx_data.getElementsByTagName('groundspeak:type')[0].firstChild.nodeValue.replace(" ","_")#.split("|")[1]
        info['container']    = gpx_data.getElementsByTagName('groundspeak:container')[0].firstChild.nodeValue.replace(" ","_")
        info['difficulty']    = gpx_data.getElementsByTagName('groundspeak:difficulty')[0].firstChild.nodeValue
        info['terrain']    = gpx_data.getElementsByTagName('groundspeak:terrain')[0].firstChild.nodeValue
        info['altname']    = gpx_data.getElementsByTagName('groundspeak:name')[0].firstChild.nodeValue
        info['placed_by']    = gpx_data.getElementsByTagName('groundspeak:placed_by')[0].firstChild.nodeValue.replace('&', '&amp;')
        info['placed_at']    = time.strftime('%d %B %Y',time.strptime(gpx_data.getElementsByTagName('time')[1].firstChild.nodeValue,'%Y-%m-%dT%H:%M:%SZ'))
    
        if gpx_data.getElementsByTagName('groundspeak:short_description')[0].attributes['html'].value == False:
            info['short_description'] = gpx_data.getElementsByTagName('groundspeak:short_description')[0].firstChild.nodeValue.strip()
        else:
            info['short_description'] = self._remove_html_tags(gpx_data.getElementsByTagName('groundspeak:short_description')[0].firstChild.nodeValue.strip())    
    
        info['long_description'] = ""
        if gpx_data.getElementsByTagName('groundspeak:long_description')[0].attributes['html'].value == False:
            info['long_description'] = gpx_data.getElementsByTagName('groundspeak:long_description')[0].firstChild.nodeValue
        else:
            info['long_description'] = self._clean_html_data(gpx_data.getElementsByTagName('groundspeak:long_description')[0].firstChild.nodeValue)
    
        info['encoded_hints']    = gpx_data.getElementsByTagName('groundspeak:encoded_hints')[0].firstChild.nodeValue.rstrip('\n      ')
        info['guid']     = gpx_data.getElementsByTagName('url')[1].firstChild.nodeValue.split("?")[1]
        
        info['logs'] = []
        for log in gpx_data.getElementsByTagName('groundspeak:log'):
            entry = dict()
            entry['type']   = log.getElementsByTagName("groundspeak:type")[0].firstChild.nodeValue
            # entry['date']   = log.getElementsByTagName("groundspeak:date")[0].firstChild.nodeValue
            entry['date']   = time.strftime('%d %B %Y at %H:%M',time.strptime(log.getElementsByTagName("groundspeak:date")[0].firstChild.nodeValue,'%Y-%m-%dT%H:%M:%SZ'))
            entry['finder'] = log.getElementsByTagName("groundspeak:finder")[0].firstChild.nodeValue
            entry['text']   = log.getElementsByTagName("groundspeak:text")[0].firstChild.nodeValue
            info['logs'].append(entry)
            

        return info
        
    def _remove_html_tags(self, data):
        if data.strip() == "":
            return
        data = self._clean_html_data(data)
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def _clean_html_data(self, data):
        if data.strip() == "":
            return
        cleaner = Cleaner(page_structure=False, links=False, style=False, safe_attrs_only=True, annoying_tags=True, allow_tags=['div', 'p', 'br'], remove_unknown_tags=False)#remove_tags=['font', 'img', 'a'])
        lxml.html.defs.safe_attrs = []
        data = cleaner.clean_html(data)
        data = data.replace("<br>", "<br />")
        data = data.encode('ascii', 'xmlcharrefreplace')
        data = data.replace("<p>&#160;</p>", "")
        return data

if __name__ == '__main__':
    print "Do not run this class directly!"

