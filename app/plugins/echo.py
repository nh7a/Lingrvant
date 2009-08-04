# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
from lingrvant import Plugin


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
    else:
      response = self.dispatch(text)
    return response

  def cmd_echo(self, argv):
    """!echo handler"""
    return ' '.join(argv)


Plugin.register(Echo())
