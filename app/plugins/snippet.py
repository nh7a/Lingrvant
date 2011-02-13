# Copyright (c) 2010 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import logging
import re
import urllib
import urllib2
from lingrvant import Plugin
from demjson import decode as decode_json


class Snippet(Plugin):
    """Web Snippet Plugin for Lingrvant"""

    def __init__(self):
        self.re_title = re.compile('<h2>(.*)<\/h2>')
        self.re_img = re.compile('<img src="(http://images.craigslist.org/[\S]*\.jpg)" alt')
        self.re_gmap = re.compile('maps.google.com/\?q=loc%3A(.*)">google map<\/a>')
        self.re_instagram = re.compile('httpinstagr.am/p/\?q=loc%3A(.*)">google map<\/a>')

    def help(self):
        """Show help"""
        return "!snippet url"

    def on_message(self, msg):
        """Message handler."""
        text = msg['text']

        match = re.match('^http://[\S]*\.craigslist.org/[\S]*\.html$', text)
        if match:
            return self.cmd_craigslist(text)

        match = re.match('^http://instagr\.am/p/[\S]*$', text)
        if match:
            return self.cmd_instagram(text)

        return self.dispatch(text)

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

    def cmd_instagram(self, url):
        params = 'url=%s' % url
        instagram = 'http://instagr.am/api/v1/oembed/?%s' % params
        logging.info('instagram: %s', instagram)
        f = urllib2.urlopen(instagram)
        buf = f.read()
        logging.info('result: %r', buf)
        res = decode_json(buf)
        logging.info('decoded: %r', res)
        return "%s\n%s" % (res['url'], res['title'])

    def cmd_fetch(self, argv):
        url = '+'.join(argv)
        if re.match('^http(?s)://', url):
            logging.info('fetch: %r', url)
            f = urllib.urlopen(url)
            buf = f.read()
            logging.info('result: size: %d', len(buf))
            logging.debug('result: %r', buf[:512])
            return '%r' % buf[:512]

Plugin.register(Snippet())
