# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib2
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
      text = ' '.join(argv[:-1])
      room = argv[-1][1:]
      url = 'http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s' % (room, config.bot_id, text, self.bot_verifier)

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
