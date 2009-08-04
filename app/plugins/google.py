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
        return self.format(r, ('titleNoFormatting', 'content', 'unescapedUrl'))

    def cmd_Gl(self, argv):
        """Local Search"""
        results = self.query('local', argv)
        a = []
        for r in results[:2]:
            s = []
            s.append(r['titleNoFormatting'])
            s.append(','.join(r['addressLines']))
            s.append(r['phoneNumbers'][0]['number'])
            s.append(r['staticMapUrl'] + '#.png')
            s.append(r['url'])
            a.append('\n'.join(s))
        s = '\n.\n'.join(a)
        s = s.replace('<b>', '').replace('</b>', '')
        return s

    def cmd_Gv(self, argv):
        """Book Search"""
        r = self.query('video', argv)
        s = self.format(r, ('titleNoFormatting', 'url'))
        s = urllib.unquote(s).replace('http://www.google.com/url?q=', '')
        return s

    def cmd_Gb(self, argv):
        """Book Search"""
        r =  self.query('blogs', argv)
        return self.format(r[:2], ('titleNoFormatting', 'content', 'postUrl'))

    def cmd_Gn(self, argv):
        """News Search"""
        r =  self.query('news', argv)
        return self.format(r[:2], ('titleNoFormatting', 'content', 'unescapedUrl'))

    def cmd_Gk(self, argv):
        """Book Search"""
        r =  self.query('books', argv)
        return self.format(r[:2], ('titleNoFormatting', 'authors', 'bookId', 'unescapedUrl'))

    def cmd_Gi(self, argv):
        """Images Search"""
        r =  self.query('images', argv)
        return self.format(r, ('contentNoFormatting', 'unescapedUrl'))

    def cmd_Gp(self, argv):
        """Patent Search"""
        results = self.query('patent', argv)
        a = []
        for r in results[:2]:
            s = []
            s.append(r['titleNoFormatting'])
            s.append('%s / %s / %s' % (r['patentNumber'], r['patentStatus'], r['applicationDate'] if 'applicationDate' in r else '-'))
            s.append(r['content'])
            s.append(r['unescapedUrl'])
            a.append('\n'.join(s))
        s = '\n.\n'.join(a)
        s = s.replace('<b>', '').replace('</b>', '')
        return s

        return self.format(r[:2], ('titleNoFormatting', 'applicationDate', 'content', 'unescapedUrl'))

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
        if len(results) == 0:
            return 'Your search did not match any documents.'

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
