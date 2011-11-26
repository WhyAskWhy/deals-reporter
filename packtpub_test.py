#!/usr/bin/python
# -*- coding: utf-8 -*-


# $Id$
# $HeadURL$

# Purpose: Fetch web page content and write matching host links to file

# TODO: Allow command-line and file input also?

# License: GPLv2

# References:
#   http://www.boddie.org.uk/python/HTML.html
#   http://stackoverflow.com/questions/753052/
#   http://www.crummy.com/software/BeautifulSoup/documentation.html
#   http://docs.python.org/library/os.html#files-and-directories
#   http://stackoverflow.com/questions/579687/
#   http://code.google.com/p/feedparser/source/browse/trunk/feedparser/feedparser.py
#   http://stackoverflow.com/questions/3947120/
#   http://www.noah.org/wiki/RegEx_Python#URL_regex_pattern
#   http://docs.python.org/library/re.html#re.findall
#   http://docs.python.org/faq/programming.html#how-do-you-remove-duplicates-from-a-list

import codecs
import sys
import os
import os.path
import re
import urllib2

import gzip
import zlib
from StringIO import StringIO

# streamWriter = codecs.lookup('utf-8')[-1]
# sys.stdout = streamWriter(sys.stdout)



from pprint import pprint as ppr

# Access to OS clipboard
from Tkinter import Tk

# http://www.crummy.com/software/BeautifulSoup/documentation.html
from BeautifulSoup import BeautifulSoup

# Prints various low level (verbose) debug statements
DEBUG_ON = True

# Prints various high level debug statements
INFO_ON = True

URL='http://www.packtpub.com/'

def clean_text(text):
    """Removes extraneous spaces, spacing, etc"""

    return str(text).replace("\r\n", "").strip()

def strip_tags(text):
    """Removes html/xml tags"""

    return ' '.join(BeautifulSoup(text).findAll(text=True))

def fetch_page(url):
    """Fetches web page and returns matched strings"""

    if INFO_ON: print "\n[I] Fetching:\t%s" % url

    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        fh = gzip.GzipFile(fileobj=buf)
        content = fh.read()
    elif zlib and 'deflate' in response.info().get('content-encoding', ''):
        try:
            content = zlib.decompress(data)
        except zlib.error, e:
            sys.exit('[E] ' + sys.exc_info()[0])
    else:
            html_page = urllib2.urlopen(url)
            content = html_page.read()
            html_page.close()

    return content


# <div class="inner"><strong>eBook Deal of the Day:<br>
# <a href="http://tinyurl.com/7gpgdle">CakePHP 1.3 Application Cookbook</a>
# </strong><div id="header-description-text">Price: $9.99 | £6.50 | €7.50<br>
# <a href="http://tinyurl.com/7gpgdle">Download a free chapter</a></div>

def pp_get_dotd(page_content):
    """Get the PacktPub eBook Deal of the Day"""

    if INFO_ON: print "\n[I] Searching for Deal of the Day ..."

    soup = BeautifulSoup(page_content)
    results = soup.find("div", { "class" : "inner" })
    #results = re.findall(r'eBook Deal of the Day.*?</a></div>', page_content, re.IGNORECASE)

    ppr(results)

    deal = BeautifulSoup(str(results)).findAll(text=True)
    ppr(deal)

    # Using commented out re.findall() call gives this:
    # -------------------------------------------------------
    # [u"['eBook Deal of the Day:",
     # u'CakePHP 1.3 Application Cookbook',
     # u'Price: $9.99 | \\xc2\\xa36.50 | \\xe2\\x82\\xac7.50',
     # u'Download a free chapter',
     # u"']"]

     # Using soup.find("div", { "class" : "inner" }) gives this:
    # -------------------------------------------------------
    # [u'eBook Deal of the Day:',
     # u'CakePHP 1.3 Application Cookbook',
     # u'Price: $9.99 | \xa36.50 | \u20ac7.50',
     # u'Download a free chapter',
     # u'Offer ends in:',
     # u'true_expires = 1322319600; countdown_expires=1794; do_offer_countdown();']

    #print "\n%s - %s" % (deal[1], deal[2][0:13])

    return deal[1], deal[2][0:13]
    
def pp_get_so(page_content):
    """Get the PacktPub Special eBook Offer"""
    
# <div id="header-offer">
# <div class="inner"><span style="font-size: 14px;"><u>
# <b>Special eBook Offer:</b></u></span><br>&nbsp;
# <br>Buy any 5 eBooks of your choice for <b>$60 | £40 | €50</b>

# - Special Offer item
    # - start of match would be Special eBook Offer
    # - end of match would be ' ' and then '|' symbol
    # - strip all html
    
    if INFO_ON: print "\n[I] Searching for Special Offers ..."

    soup = BeautifulSoup(page_content)
    
    #results = soup.find("div", { "id" : "header-offer" })
    results = soup.find("div", { "id" : "block-block-114" })
    
    #results = re.findall(r'eBook Deal of the Day.*?</a></div>', page_content, re.IGNORECASE)

    #print "results: "
    #ppr(results)

    deal = BeautifulSoup(str(results)).findAll(text=True)
    print "deal: "
    ppr(deal)
    
    for item in deal:
        #item = item.strip('[]').replace(u'\r', '').replace(u'\n', '')
        print item
        
    print "results after cleanup: "
    ppr(deal)

    #deal = clean_text(strip_tags(str(results)))


    # [u'Special eBook Offer:',
     # u'&nbsp;',
     # u'Buy any 5 eBooks of your choice for ',
     # u'$60 | \xc2\u014140 | \xe2&sbquo;\u017950',
     # u'.',
     # u'View all Latest books',
     # u'&nbsp;|&nbsp;',
     # u'View all Future books']
    # (u'&nbsp;', u'Buy any 5 eBo')

    #print "\n%s - %s" % (deal[1], deal[2][0:13])

    return deal
    #return "%s %s %s" % (deal[1].strip(), deal[3].strip(), deal[4][:4].strip())

def main():

        page_content = fetch_page(URL)
        #deal = pp_get_dotd(page_content)
        special_offer = pp_get_so(page_content) 


        print special_offer



if __name__ == "__main__":
    main()
