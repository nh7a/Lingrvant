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

  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.headers['charset'] = 'utf-8'
    self.response.set_status(200)

    try:
      json = self.request.get("json")
      logging.debug("json: %s" % json)
      if len(json) > 0:
        param = decode_json(json)
        for event in param['events']:
          self.on_message(event['message'])
      else:
        text = urllib.unquote(self.request.get("text"))
        self.on_message({'text':text})

    except Exception, e:
      logging.error(e)

  def on_message(self, message):
    write = self.response.out.write
    logging.info("text: %s" % message['text'])

    for plugin in Plugin.plugins:
      response = plugin.on_message(message)
      if response:
        logging.info("response: %s" % response)
        write(response)


class LingrvantHomepage(webapp.RequestHandler):
  def get(self, msg):
    write = self.response.out.write
    write("OkOk")


def main():
  Plugin.load()
  application = webapp.WSGIApplication([('/handler', LingrvantHandler),
                                        ('/(.*)', LingrvantHomepage)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
