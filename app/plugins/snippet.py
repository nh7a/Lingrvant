# Copyright (c) 2010 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
from lingrvant import Plugin


class Snippet(Plugin):
    """Web Snippet Plugin for Lingrvant"""

    def __init__(self):
        self.re_title = re.compile('<h2>(.*)<\/h2>')
        self.re_img = re.compile('<img src="(http://images.craigslist.org/[\S]*\.jpg)" alt')
        self.re_gmap = re.compile('maps.google.com/\?q=loc%3A(.*)">google map<\/a>')

    def help(self):
        """Show help"""
        return "!snippet url"

    def on_message(self, msg):
        """Message handler."""
        text = msg['text']

        match = re.match('^http://[\S]*\.craigslist.org/[\S]*\.html$', text)
        if match:
            response = self.cmd_craigslist(text)
        else:
            response = self.dispatch(text)
        return response

    def cmd_craigslist(self, url):
        """!snippet handler"""
        result = []
        f = urllib.urlopen(url, '')
        q = f.read()
        m = self.re_title.search(q)
        if m:
            result.append(m.group(1))
        m = self.re_gmap.search(q)
        if m:
            result.append('http://maps.google.com/maps/api/staticmap?zoom=15&size=640x320&markers=%s&sensor=false&n.gif' % m.group(1))
        m = self.re_img.findall(q)
        if m:
            for i in m:
                result.append(i)

        return "\n".join(result)

Plugin.register(Snippet())
