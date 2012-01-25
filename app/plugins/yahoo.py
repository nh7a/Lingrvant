# Copyright (c) 2012 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
from lingrvant import Plugin

class Yahoo(Plugin):
  """Yahoo Plugin for Lingrvant"""

  def help(self):
    """Show help."""
    return """!yf (symbol)"""

  def on_message(self, msg):
    """Message handler."""
    text = msg['text']

    if re.match('^\$\w+$', text):
      response = self.cmd_yf([text[1:]])
    else:
      response = self.dispatch(text)
    return response

  def cmd_yf(self, symbol):
    return 'http://chart.finance.yahoo.com/z?s=%s&.png' % symbol[0]


Plugin.register(Yahoo())
