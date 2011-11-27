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
#   http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python

import codecs
import sys
import os
import os.path
import re
import urllib2

import gzip
import zlib
from StringIO import StringIO

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)



from pprint import pprint as ppr

# http://www.crummy.com/software/BeautifulSoup/documentation.html
from BeautifulSoup import BeautifulSoup

# Prints various low level (verbose) debug statements
DEBUG_ON = True

# Prints various high level debug statements
INFO_ON = True

URL='http://www.packtpub.com/'


def clean_text(text):
    """Removes extraneous spaces, spacing, etc"""

    regex = re.compile(r'\n*\t*\[*\]*')
    return regex.sub('', text).strip()


#    for i, j in dic.iteritems():
#       text = text.replace(i, j).strip()
#    return text

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
    
    dotd_marker = 'eBook Deal of the Day'

    soup = BeautifulSoup(page_content)
    results = soup.find("div", { "class" : "inner" })
    #results = re.findall(r'eBook Deal of the Day.*?</a></div>', page_content, re.IGNORECASE)

    deal = BeautifulSoup(str(results)).findAll(text=True)
    
    if DEBUG_ON:
        print "\n    What was found: "
        ppr(deal, indent=4)

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

    if dotd_marker in deal[0]:
        return deal[1], deal[2][0:13]
    else:
        if INFO_ON: print "\n[W] Deal of the Day was not found"
        return False

def pp_get_so(page_content):
    """Get the PacktPub Special eBook Offer"""
    
    # String we're matching on to determine whether an offer is available
    so_marker = 'Special eBook Offer'
    
# <div id="block-block-114" class="block block-block region-even odd region-count-4 count-9">
# ...
# </div>
    
    if INFO_ON: print "\n[I] Searching for Special Offers ..."

    soup = BeautifulSoup(page_content)
    results = soup.find("div", { "id" : "block-block-114" })

    text = BeautifulSoup(str(results)).findAll(text=True)
    if DEBUG_ON: 
        print "\ntext: "
        ppr(text)
        print "\n\n"

    string = ''.join(text)
    deal = clean_text(string)

    if so_marker in deal:
        return deal.replace(so_marker,'').strip()
    else:
        if INFO_ON: print "\n[W] Special eBook Offer not found"
        return False

def main():

        page_content = fetch_page(URL)
        deal = pp_get_dotd(page_content)
        special_offer = pp_get_so(page_content) 

        if deal:
            print "[I] The eBook Deal of the Day is: \n\t%s" % deal

        if special_offer:
            print "[I] The Special eBook Offer is: \n\t%s" % special_offer



if __name__ == "__main__":
    main()
