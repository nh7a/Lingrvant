# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import logging
import os
import sys
import re
import urllib
import hashlib
import config
try:
  from google.appengine.api import memcache as memcache_
except:
  pass

class Plugin:
  """Lingr Plugin base class"""
  plugins = []

  @property
  def memcache(self):
    try:
      return memcache_
    except:
      class dummy:
        def set(self, key, namespace): pass
        def get(self, key, namespace): return False
        def delete(self, key, namespace): pass
      return dummy()

  def name(self):
    """Show name of plugin"""
    name = str(self)
    m = re.search('\.([a-zA-Z]+) instance', str(self))
    return m.group(1)

  def help(self):
    """Show help"""
    pass

  def on_message(self, msg):
    """Message handler."""
    return self.dispatch(msg['text'])

  def dispatch(self, msg):
    """Message dispatcher."""
    if len(msg) == 0 or msg[0] != "!":
      return
    argv = msg.split(' ')
    if len(argv) == 0:
      return

    if argv[0] == msg:
      argv = msg.split('.')  # hack!

    try:
      command = argv[0].strip()
      func = getattr(self, "cmd_%s" % command[1:])
      if len(argv) == 1:
        return func([])
      else:
        return func(argv[1:])
    except AttributeError:
      pass
    except Exception, e:
      print e

  def escape(self, s):
    """Escape an URL."""
    return urllib.quote(s, safe='~')

  def utf8_str(self, s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    else:
        return str(s)

  @classmethod
  def register(cls, plugin):
    """Register plugin."""
    cls.plugins.append(plugin)

  @classmethod
  def load(cls):
    """Load all plugins."""
    plugins_root = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(plugins_root):
      return

    for plugin in os.listdir(plugins_root):
      plugin = re.search('^([a-zA-Z0-9]\w+).py$', plugin)
      if plugin:
        try:
          exec('from plugins import %s' % plugin.group(1))
          logging.debug('imported plugin: %s' % plugin.group(1))
        except Exception, e:
          logging.error(e)

  @property
  def bot_verifier(self):
    if not hasattr(self, "bot_verifier_"):
      self.bot_verifier_ = hashlib.sha1(config.bot_id + config.bot_secret).hexdigest()
    return self.bot_verifier_
