# Copyright (c) 2012 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import urllib
import logging
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

    if re.match('^\$[\w=]+$', text):
      response = self.cmd_yf([text[1:]])
    else:
      response = self.dispatch(text)
    return response

  def cmd_yf(self, symbol):
    chart = 'http://chart.finance.yahoo.com/z?s=%s&t=1y&q=l&l=on&z=l&p=m50,e200,v&.png' % symbol[0]
    q = self.get_quotes(symbol[0])
    if q:
      s = '%s\n%s (%s)\n%s %s (%s)\nP/E: %s' % (chart, q['name'], q['symbol'], q['last trade'], q['change'][0], q['change'][1], q['p/e'])
    else:
      s = chart
    return s

  def get_quotes(self, symbol):
    try:
      params = urllib.urlencode({'s': symbol, 'f':'snl1crx'})
      url = 'http://download.finance.yahoo.com/d/quotes.csv?'
      f = urllib.urlopen(url + params)
      res = f.read().rstrip().split(',')
      if int(res[2]) == 0: return
      # ['"LNKD"', '"LinkedIn Corporat"', '89.11', '"+12.72 - +16.65%"', '1046.44']
      return {'symbol': res[0].strip('"'),
              'name': res[1].strip('"'),
              'last trade': res[2],
              'p/e': res[4],
              'change': res[3].strip('"').split(' - ')}
    except:
      pass

Plugin.register(Yahoo())
