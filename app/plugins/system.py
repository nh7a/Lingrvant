# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
from lingrvant import Plugin


class System(Plugin):

  def help(self):
    """Show help"""
    return """!list
!help [module name]"""

  def cmd_help(self, argv):
    """!help handler."""
    if len(argv):
      for plugin in Plugin.plugins:
        if argv[0].lower() == plugin.name().lower():
          return plugin.help()
    return self.help()

  def cmd_list(self, argv):
    """!list handler."""
    msg = []
    for plugin in Plugin.plugins:
      msg.append(plugin.name())
    return ', '.join(msg)


Plugin.register(System())
