#!/usr/bin/python

# $Id$
# $HeadURL$

# Purpose: Fetch Deal of the Day/Week from vendors and send email notifications.

# License: GPLv2

# References:
# http://docs.python.org/library/smtplib.html
# http://docs.python.org/library/email-examples.html
# http://effbot.org/pyfaq/how-do-i-send-mail-from-a-python-script.htm
# http://www.answermysearches.com/how-to-get-a-month-name-in-python/421/
# http://docs.python.org/library/datetime.html
# http://www.boddie.org.uk/python/HTML.html
# http://stackoverflow.com/questions/753052/
# http://gomputor.wordpress.com/2008/09/27/search-replace-multiple-words-or-characters-with-python/
# http://docs.python.org/faq/programming.html#how-do-you-remove-duplicates-from-a-list
# http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

import datetime
import gzip
import zlib
from StringIO import StringIO

import urllib2

# http://www.crummy.com/software/BeautifulSoup/documentation.html
from BeautifulSoup import BeautifulSoup

DEBUG_ON = False
INFO_ON = False

FROM_ADDR = "deals@example.com"
TO_ADDR   = 'root'
DATE = datetime.date.today()
SUBJECT = "eBook Deals for %s" % DATE

# Single email or one email per SITE entry
SINGLE_EMAIL= True

# Not implemented yet
USE_DEAL_IN_SUBJECT=False

SITES = [
        {
            'url': 'http://feeds.feedburner.com/oreilly/mspebookdeal?format=xml',
            'alt_url': 'http://oreilly.com/',
            'tag': 'title',
            'skip_first_tag': True,
            'name': 'Microsoft Press',
        },
        {
            'url': 'http://feeds.feedburner.com/oreilly/ebookdealoftheday?format=xml',
            'alt_url': 'http://oreilly.com/',
            'tag': 'title',
            'skip_first_tag': True,
            'name': "O'Reilly Media",
        },
        {
            'url': 'http://incsrc.manningpublications.com/dotd.js',
            'alt_url': 'http://www.manning.com/',
            'tag': None,
            'skip_first_tag': False,
            'name': 'Manning Books',
        },
        {
            'url': 'https://www.apress.com/index.php/dailydeals/index/rss', 
            'tag': 'title',
            'skip_first_tag': True,
            'name': 'Apress',
        },
        {
            'url': 'http://www.peachpit.com/deals/index.aspx', 
            'tag': 'h1',
            'skip_first_tag': False,
            'name': 'Peachpit',
        },
        {
            'url': 'http://www.informit.com/deals/index.aspx', 
            'tag': 'h1',
            'skip_first_tag': False,
            'name': 'Informit',
        },
        {
            'url': 'http://www.quepublishing.com/deals/index.aspx', 
            'tag': 'h1',
            'skip_first_tag': False,
            'name': 'Que Publishing',
        },
]



def clean_text(text):
    """Removes extraneous spaces, spacing, etc"""

    regex = re.compile(r'\n*\t*\[*\]*')
    return regex.sub('', text).strip()


def strip_tags(text):
    """Removes html/xml tags"""

    return ' '.join(BeautifulSoup(text).findAll(text=True))

def js_strip(text):
    """Temporary function to remove JavaScript content from
    text"""

    return text.replace('document.write', '').strip('"()')

def fetch_page(site):
    """Fetches web page content"""

    if INFO_ON: print "\n[I] Fetching:\t%s" % site['url']

    request = urllib2.Request(site['url'])
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
            html_page = urllib2.urlopen(site['url'])
            content = html_page.read()
            html_page.close()

    return content

def get_deal(site, page_content):
    """Parses web page content and returns matched strings"""

    soup = BeautifulSoup(page_content)

    if site['tag'] is not None:
        if site['skip_first_tag']:
            item = soup.findAll(site['tag'])[1]
        else:
            item = soup.findAll(site['tag'])[0]

        item = strip_tags(clean_text(item))

    # tag isn't set, so we're cleaning and using all of the input
    # text for the item we're reporting as a deal
    else:
        item = js_strip(strip_tags(clean_text(soup)))

    return item



def prep_msg(site_names, matches, urls):
    """Prepares a string to deliver to the send_email function"""

    content = ""

    # Assume every match has a corresponding url

    if SINGLE_EMAIL:
        for site_name, match, url in map(None, site_names, matches, urls):
                content +="\n\n\n%s:\n\t%s\n\n\t%s" % (str(site_name), str(match), str(url))
    else:
        content = "\n\n\n%s:\n\t%s\n\n\t%s" % (str(site_names), str(matches), str(urls))

    msg = MIMEText(content)
    return msg

def send_email(to_addr, from_addr, subject, msg, site_name=""):
    """Receives everything necessary to send an email"""

    if SINGLE_EMAIL:
        msg['Subject'] = "%s" % subject
    else:
        msg['Subject'] = "%s %s" % (site_name, subject)

    msg['From'] = from_addr
    msg['To'] = to_addr

    # Send the message via our own SMTP server, but don't include the envelope header.
    server = smtplib.SMTP('localhost')
    #server.set_debuglevel(1)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

def main():


    if SINGLE_EMAIL:

        sites, matches, urls = [], [], []

        # http://docs.python.org/tutorial/datastructures.html#looping-techniques
        for site in SITES:
            sites.append(site['name'])
            site_content = fetch_page(site)
            deal = get_deal(site, site_content)
            matches.append(deal)

            # If an alternate url exists, pass that instead of the feed url
            if 'alt_url' in site:
                urls.append(site['alt_url'])
            else:
                urls.append(site['url'])

        # Convert deals (and their urls) into a MIME compliant email format.
        message = prep_msg(sites, matches, urls)


        if DEBUG_ON:
            print "\n%s\n%s" % (SUBJECT, message)
        else:
            send_email(TO_ADDR, FROM_ADDR, SUBJECT, message)
    else:

        # http://docs.python.org/tutorial/datastructures.html#looping-techniques
        for site in SITES:
            site_content = fetch_page(site)
            match = get_deal(site, site_content)

            # Convert deals (and their urls) into a MIME compliant email format.
            # If an alternate url exists, pass that instead of the feed url
            if 'alt_url' in site:
                url = site['alt_url']
            else:
                url = site['url']

            message = prep_msg(site['name'], match, url)

            if DEBUG_ON:
                print "\n\n%s %s\n%s" % (site['name'], SUBJECT, message)
            else:
                send_email(TO_ADDR, FROM_ADDR, SUBJECT, message, site['name'])

if __name__ == "__main__":
    main()
