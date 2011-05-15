#!/usr/bin/env python
# encoding: utf-8
"""
gpx2epub.py

Created by Frank Rosquin.

Copyright (c) 2011, Frank Rosquin <frank.rosquin@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import sys
import os

import argparse

from gcache2ebook.convert import Convert


def main():
    parser = argparse.ArgumentParser(description='Create an ePub from some GPX files.')
    parser.add_argument('--gpx', dest='gpx_dir', action='store', default='~/Documents/GeoCaching/GPX/',
                        help='place where the GPX files are (default: ~/Documents/GeoCaching/GPX/)')
    
    parser.add_argument('output', metavar='OUTPUT', type=str, nargs='?', default='~/Documents/GeoCaching/', 
                        help='Place to put the ePub (default: ~/Documents/GeoCaching/)')
    args = parser.parse_args()
    
    
    convertor = Convert("gpx", "epub")
    convertor.output_file   = args.output
    convertor.cache_source  = os.path.expanduser(args.gpx_dir)
    # convertor.status()
    convertor.start()
    convertor.done()



if __name__ == '__main__':
    main()

