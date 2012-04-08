$Id$
$HeadURL$

Deal Mailer VERSION_PLACEHOLDER
Deoren Moor
http://projects.whyaskwhy.org/

Description, Usage, Requirements, Install, Contact us, Bugs, Copyright, License.


==================
DESCRIPTION
==================

Deal Mailer is a Python script that fetches the latest deals (currently only for ebooks)
and sends an email notification.


==================
USAGE
==================

The idea is to run it via a cron job daily to see if there are any deals you may be
interested in. To do this, you'll need to specify several settings which are mentioned
below.


==================
REQUIREMENTS 
==================

- Python 2.6.x
    http://www.python.org/download/releases/
    http://www.python.org/ftp/python/

- Beautiful Soup
    http://www.crummy.com/software/BeautifulSoup/

    Note: Has it's own license. See 'License' at the bottom of this file.


==================
INSTALLATION
==================

- Beautiful Soup

    If you're running at least Ubuntu 10.04, this should take care of you:

        apt-get install python-beautifulsoup

- The Deal Mailer script:

    Copy it somewhere where you keep other scripts that are not provided
    by the operating system. For example, /usr/local/bin/ or your home
    directory.

    Configure the script to include at least this basic information:

        * Mail server
        * Email address (who is going to receive it?)
        * Sender address (what address do you want to claim is sending it?)

See http://projects.whyaskwhy.org/projects/deal-mailer/wiki/ for more details.


==================
CONTACT US
==================

We look forward to hearing from you!

 Project homepage: http://projects.whyaskwhy.org/
           Forums: http://projects.whyaskwhy.org/projects/deal-mailer/boards


==================
BUGS
==================

Before submitting a bug, please:

#1) Make sure you are running the latest version of Deal Mailer.

#2) Check the forums to see if someone else has already reported the problem.
    http://projects.whyaskwhy.org/projects/deal-mailer/boards

#3) Search for an existing issue that matches your problem.
    http://projects.whyaskwhy.org/search/index/deal-mailer?issues=1

#4) If none of the above are true, please submit a bug and include as much
    relevant information as you can to help with fixing it.

Thanks!


==================
COPYRIGHT (Deal Mailer)
==================

Copyright (C) 2012 deoren of WhyAskWhy.org


==================
LICENSING
==================

Deal Mailer is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
version 2 of the License.

Deal Mailer is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Deal Mailer. If not, see http://www.gnu.org/licenses/

You may also refer to license.txt that is included within this code repository.
