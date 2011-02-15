# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib, urllib2
from lingrvant import Plugin
import config
from demjson import decode as decode_json


class Echo(Plugin):
  """Echo Plugin for Lingrvant"""

  def help(self):
    """Show help."""
    return "!echo foo"

  def on_message(self, msg):
    """Message handler."""
    text = msg['text']

    if re.match('^helo\s*$', text):
      response = '250'
    elif re.match('^ehlo\s*$', text):
      response = """250-AUTH LOGIN CRAM-MD5 PLAIN
250-AUTH=LOGIN CRAM-MD5 PLAIN
250-STARTTLS
250-PIPELINING
250 8BITMIME"""
    elif re.match('^[.0-9\(\)\+\-/\*\s]+\s*=$', text):
      try:
        response = str(eval('(%s)' % text[:-1]))
      except:
        pass
    else:
      response = self.dispatch(text)
    return response

  def cmd_echo(self, argv):
    """!echo handler"""
    if re.match('^@[a-zA-Z]+$', argv[-1]):
      params = {'text':' '.join(argv[:-1]).encode('utf-8'),
                'room':argv[-1][1:],
                'bot':config.bot_id,
                'bot_verifier':self.bot_verifier}
      url = 'http://lingr.com/api/room/say?' + urllib.urlencode(params)
      try:
        f = urllib2.urlopen(url)
        res = decode_json(f.read())
        if res['status'] == 'ok':
          result = 'Posted'
        else:
          result = res['detail']
      except Exception, e:
        result = str(e)
    else:
      result = ' '.join(argv)

    return result

Plugin.register(Echo())
