# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import os, sys
import logging
import urllib
import wsgiref.handlers

from google.appengine.ext import webapp
from lingrvant import Plugin

APP_DIRECTORY = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(APP_DIRECTORY, 'third_party'))

from demjson import decode as decode_json


class LingrvantHandler(webapp.RequestHandler):
  def __init__(self):
    Plugin.load()

  def get(self, msg):
    write = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.headers['charset'] = 'utf-8'
    self.response.set_status(200)

    if len(msg) == 0:
      write('OkOk')
      return

    try:
      json = self.request.get("json")
      if len(json) > 0:
        param = decode_json(json)
        msg = param['events'][0]['message']['text']
      else:
        msg = urllib.unquote(msg)
      logging.error("msg: %s" % msg)

      for plugin in Plugin.plugins:
        response = plugin.on_message(msg)
        if response:
          logging.error("response: %s" % response)
          write(response)

    except Exception, e:
      logging.error(e)


def main():
  application = webapp.WSGIApplication([('/(.*)', LingrvantHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
