# Copyright (c) 2010 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
from lingrvant import Plugin
from demjson import decode as decode_json

class DuckDuckGo(Plugin):
    """DuckDuckGo search Plugin for Lingrvant"""

    def help(self):
        """Help"""
        return """!D query..."""

    def cmd_D(self, argv):
        """Web Search"""
        r = self.query('web', argv)
        text = ''
        if len(r['AbstractText']) > 0:
            text = r['AbstractText']
        elif len(r['RelatedTopics']) > 0:
            text = r['RelatedTopics'][0]['Text']
            if 'FirstURL' in r['RelatedTopics'][0]:
                text += " " + r['RelatedTopics'][0]['FirstURL']
        elif len(r['Results']) > 0:
            text = r['Results'][0]['Text']
            if 'FirstURL' in r['Results'][0]:
                text += " " + r['Results'][0]['FirstURL']
        else:
            return 'dunno nuttin bout it'
        text += " - Powered by Duck Duck Go"
        if 'Image' in r:
            text += "\n" + r['Image']
        return text

    def query(self, property, argv):
        """Make a query to DuckDuckGo."""
        if argv == None:
            return

        query = ' '.join(argv)
        params = {'o': 'json', 'q': self.utf8_str(query)}
        url = 'http://duckduckgo.com/?'
        params = urllib.urlencode(params)
        f = urllib.urlopen(url + params)
        return decode_json(f.read())


Plugin.register(DuckDuckGo())
