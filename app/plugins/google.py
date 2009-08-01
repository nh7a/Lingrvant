# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
from lingrvant import Plugin
from demjson import decode as decode_json


class Google(Plugin):
    """Google search Plugin for Lingrvant"""

    def help(self):
        """Help"""
        return """!G[wlvbnkip] query...
w: Web Search
l: Local Search
v: Video Search
b: Blog Search
n: News Search
k: Book Search
i: Image Search
p: Patent Search"""

    def cmd_G(self, argv):
        """Default (web) Search"""
        return self.cmd_Gw(argv)

    def cmd_Gw(self, argv):
        """Web Search"""
        r = self.query('web', argv)
        return self.format(r, ('titleNoFormatting', 'content', 'url'))

    def cmd_Gl(self, argv):
        """Local Search"""
        r = self.query('local', argv)
        return self.format(r, ('titleNoFormatting', 'url'))

    def cmd_Gv(self, argv):
        """Book Search"""
        r = self.query('video', argv)
        s = self.format(r, ('titleNoFormatting', 'url'))
        s = urllib.unquote(s).replace('http://www.google.com/url?q=', '')
        return s

    def cmd_Gb(self, argv):
        """Book Search"""
        r =  self.query('blogs', argv)
        return self.format(r, ('titleNoFormatting', 'content', 'postUrl'))

    def cmd_Gn(self, argv):
        """News Search"""
        r =  self.query('news', argv)
        return self.format(r, ('titleNoFormatting', 'content', 'url'))

    def cmd_Gk(self, argv):
        """Book Search"""
        r =  self.query('books', argv)
        return self.format(r, ('titleNoFormatting', 'authors', 'bookId', 'url'))

    def cmd_Gi(self, argv):
        """Images Search"""
        r =  self.query('images', argv)
        return self.format(r, ('contentNoFormatting', 'url'))

    def cmd_Gp(self, argv):
        """Patent Search"""
        r = self.query('patent', argv)
        return self.format(r, ('titleNoFormatting', 'content', 'url'))

    def query(self, property, argv):
        """Make a query to Google property."""
        hl = 'en'
        if argv[0][0:3] == 'hl=':
            hl = argv[0][3:]
            del argv[0]

        if argv == None:
            return

        query = ' '.join(argv)
        params = {'v': '1.0', 'hl':hl, 'q': self.utf8_str(query)}

        url = 'http://ajax.googleapis.com/ajax/services/search/%s?' % property
        params = urllib.urlencode(params)
        f = urllib.urlopen(url + params)
        res = decode_json(f.read())
        return res['responseData']['results']

    def format(self, results, items):
        """Format output text accordingly."""
        a = []
        for r in results:
            s = []
            for i in items:
                s.append(r[i])
            a.append('\n'.join(s))
        s = '\n.\n'.join(a)
        s = s.replace('<b>', '').replace('</b>', '')
        return s


Plugin.register(Google())
