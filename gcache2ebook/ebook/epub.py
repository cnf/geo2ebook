#!/usr/bin/env python
# encoding: utf-8
"""
ePub.py

Created by Frank Rosquin on 2009-09-01.
Copyright (c) 2009 frank.rosquin.net. All rights reserved.
"""

import sys
import os
import os.path
import shutil
import re
import urllib
from datetime import date

from mako.template import Template
from gcache2ebook.tools import base_path

class ePub:
    def __init__(self, tmp_path):
        self.tmp_path       = tmp_path + "/ePub"
        self.pages_path     = self.tmp_path + "/pages"
        self.build_path     = self.tmp_path + "/build"
        os.mkdir(self.tmp_path)
        self.output_file    = ""
        self.author = "GeoCaching.com"
        self.title = "GeoCaches"
    
    def create(self, cache_data):
        """docstring for create"""
        os.mkdir(self.pages_path)
        cache_list = []
        for cache in cache_data:
            cache_list.append(self._create_page(cache))
        self.prep_dir()
        self.get_parts(cache_list)
        self.gen_toc(cache_list)
        self.create_book()
        
    def _create_page(self, cache):
        """docstring for _create_page"""
        html = Template(filename=base_path() + '/resources/templates/epub.html')
        output = html.render(**cache)
        # print 'Generating ' + os.path.basename(fileName)
        tmp_file = self.pages_path + '/' + cache['name'] + '.html'
        with open(tmp_file, 'w') as f:
            f.write('')
            f.write(output.encode('ascii', 'xmlcharrefreplace'))
        return cache['name']
    
    def prep_dir(self):
        """docstring for prepDir"""
        # setup all the file directories and default files
        os.mkdir(self.build_path)
        os.mkdir(self.build_path + '/META-INF')
        os.mkdir(self.build_path + '/OEBPS')
        os.mkdir(self.build_path + '/OEBPS/css')
        #os.mkdir(self.tmp_path + '/OEBPS/img')
        shutil.copytree(base_path() + '/resources/images', self.build_path + '/OEBPS/img')
        shutil.copyfile(base_path() + '/resources/templates/uitleg.html', self.build_path + '/OEBPS/uitleg.html')
        
        
        # Style sheet to use (todo allow people to pass in their own)
        myStyle = """@page {margin-top: 0.8em; margin-bottom: 0.8em;}\n.titleimg {text-align:center;}"""
        open(self.build_path + "/OEBPS/css/main.css", "w").write(myStyle)
        open(self.build_path + "/mimetype", "w").write("application/epub+zip")
        
        containerXml= (
        '<?xml version="1.0" ?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '<rootfiles>\n'
        '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />\n'
        '</rootfiles>\n'
        '</container>\n' )
        open(self.build_path + "/META-INF/container.xml","w").write(containerXml)
    
    
    def get_parts(self, cache_list):
        """docstring for getParts"""
        for cache in cache_list:
            file_name = self.pages_path + '/' + cache + '.html'
            shutil.copyfile(file_name, self.build_path + '/OEBPS/' + cache + '.html')
    
    
    def gen_toc(self, sections):
        """docstring for genTOC"""
        count = 1
        opf1 = '<opf:item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'
        opf1 = opf1 + '<opf:item id="TableOfContents" href="TableOfContents.html" media-type="application/xhtml+xml" />\n'
        opf2 = "<opf:itemref idref=\"TableOfContents\"/>\n"
        
        opf1 = opf1 + "<opf:item id=\"%s\" href=\"%s\" media-type=\"application/xhtml+xml\"/>\n" % ('uitleg', 'uitleg.html')
        opf2 = opf2 + "<opf:itemref idref=\"%s\"/>\n" % ('uitleg')
        toc1 = '<li><a href="%s">%s</a> </li>\n' % ('uitleg.html', 'Wat is GeoCaching?')
        
        tocOut = ( '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="en" version="2005-1">\n\n'
        '<head>\n'
        '<meta name="dtb:uid" content="b0f76506-7763-11dd-83b7-001cc05a7670"/>\n'
        '<meta name="dtb:depth" content="1"/>\n'
        '<meta name="dtb:totalPageCount" content="0"/>\n'
        '<meta name="dtb:maxPageNumber" content="0"/>\n'
        '</head>\n\n'
        '<docTitle>\n'
        '<text>%s</text>\n'
        '</docTitle>\n'
        '<navMap>\n' ) % self.title
        
        tocOut = tocOut + (
        '<navPoint id="part%d" playOrder="%d">\n'
        '<navLabel>\n'
        '<text>%s</text>\n'
        '</navLabel>\n'
        '<content src="%s"/>\n'
        '</navPoint>\n' ) % (count, count, 'Wat is GeoCaching?' , 'uitleg.html')
        
        contentHeader = ( '<?xml version="1.0" encoding="UTF-8" ?>\n'
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n\n'
        '<head>\n'
        '<title>%s</title>\n'
        '<link rel="stylesheet" href="css/main.css" type="text/css" />\n'
        '<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />\n'
        '</head>\n\n'
        '<body>\n'
        '<div class="titleimg"><img src="img/GeoCaching.png" /> &nbsp;<img src="img/CacheInTrashOut.gif" /></div>\n'
        '<h1>List of Caches</h1>\n'
        '<h3>From www.geocaching.com</h3>\n'
        '<ul>' ) % self.title 
        
        
        
        # for each section create an entry in the TOC for it, and then write it to disk
        for section in sections:
            tocOut = tocOut + (
            '<navPoint id="part%d" playOrder="%d">\n'
            '<navLabel>\n'
            '<text>%s</text>\n'
            '</navLabel>\n'
            '<content src="%s"/>\n'
            '</navPoint>\n' ) % (count, count, section , section + '.html')
            
            # create some xml indexing
            opf1 = opf1 + "<opf:item id=\"%s\" href=\"%s\" media-type=\"application/xhtml+xml\"/>\n" % (section, section + '.html')
            opf2 = opf2 + "<opf:itemref idref=\"%s\"/>\n" % (section)
            toc1 = toc1 + '<li><a href="%s">%s</a> </li>\n' % (section + '.html', section)
            count = count + 1
            
        tocOut = tocOut + "</navMap></ncx>"
        
        contentOpf = ( '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<opf:package version="2.0" unique-identifier="dcid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '<opf:metadata>\n'
        '<dc:identifier id="dcid" opf:scheme="UUID">urn:uuid:3675ff2a-3059-4102-a2f4-30ab059267ed</dc:identifier>\n'
        '<dc:title>%s</dc:title>\n'
        '<dc:creator>%s</dc:creator>\n'
        '<dc:language>English</dc:language>\n'
        '<dc:subject>A Book of Caches from Geocaching.com</dc:subject>\n'
        '<dc:description>This book has been generated from GPX files downloaded from Geocaching.com, in an effort to go paperless</dc:description>\n'
        '<dc:date opf:event="modification">%s</dc:date>\n'
        '</opf:metadata>\n' 
        '<opf:manifest>\n'
        '%s'
        '</opf:manifest>\n'
        '<opf:spine toc="ncx">\n'
        '%s'
        '</opf:spine>\n'
        '</opf:package>') % (self.title, self.author, date.today(), opf1, opf2)
        
        open(str(self.build_path) + "/OEBPS/toc.ncx", "w").write(tocOut)
        open(str(self.build_path) + "/OEBPS/content.opf","w").write(contentOpf)
        open(str(self.build_path) + "/OEBPS/TableOfContents.html", "w").write(contentHeader + toc1 + '</ul></body></html>')
    
    
    def create_book(self):
        """docstring for createBook"""
        # now package everything up
        os.system("cd %s ; zip -q -X %s.zip -n mimetype mimetype  ; zip %s.zip -q -r META-INF/ OEBPS/ ; mv %s.zip %s.epub; mv %s.epub %s/" % (self.build_path, self.title, self.title, self.title, self.title, self.title, self.output_file) )

# end of genepub