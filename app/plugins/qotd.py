# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
from lingrvant import Plugin


class QOTD(Plugin):
    """Quote of the Day Plugin for Lingrvant"""

    def __init__(self):
        self.re_tag = re.compile('<[a-zA-Z\/][^>]*>')
        self.re_quote = re.compile('<dt class="quote">(.*)<\/dt><dd class="author">(.*)<\/dd>')

    def help(self):
        """Show help"""
        return "!Q"

    def cmd_Q(self, argv):
        """!Q handler"""
        url = 'http://www.quotationspage.com/random.php3'
        params = {}
        params['number'] = 4
        params['collection[]'] = 'mgm'
        params['collection[]'] = 'motivate'
        params['collection[]'] = 'classic'
        params['collection[]'] = 'coles'
        params['collection[]'] = 'lindsly'
        params['collection[]'] = 'poorc'
        params['collection[]'] = 'altq'
        params['collection[]'] = '20thcent'
        params['collection[]'] = 'bywomen'
        params['collection[]'] = 'devils'
        params['collection[]'] = 'contrib'
        params = urllib.urlencode(params)
        f = urllib.urlopen(url, params)
        q = f.read()
        m = self.re_quote.search(q)
        if m:
            quote = self.remove_tags(m.group(1))
            author = self.remove_tags(m.group(2))
            return "%s --- %s" % (quote, author)
        return 'no quote found'

    def remove_tags(self, html):
        """Remove HTML tags and leading/trailing spaces."""
        return self.re_tag.sub('', html).strip()


Plugin.register(QOTD())
