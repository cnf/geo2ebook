#!/usr/bin/env python
# encoding: utf-8
"""
convert.py

Created by Frank Rosquin on 2011-03-12.
Copyright (c) 2011 Frank Rosquin. All rights reserved.
"""

import sys
import os
import tempfile
import shutil
from cache.gpx import GPX
from ebook.epub import ePub


class Convert:
    def __init__(self, input_format="gpx", output_format="epub"):
        self.input_format       = input_format
        self.output_format      = output_format
        self.output_file        = ""
        self.consolidate        = True
        self.tmp_path           = tempfile.mkdtemp()
        
        self.cache_source       = ""
        # self.__del__()
    
    def __del__(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
    
    def start(self):
        if self.input_format == "gpx":
            geocache = GPX()
            geocache.cache_source = self.cache_source
        if self.output_format == "epub":
            ebook = ePub(self.tmp_path)
            ebook.output_file = self.output_file
        geocache.extract()
        ebook.create(geocache.cache_data)
    
    def done(self):
        """docstring for done"""
        print "You can find your eBook at {0}GeoCaching.{1}".format(self.output_file, self.output_format)
        pass
            

    def status(self):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.__dict__)


if __name__ == '__main__':
    pass