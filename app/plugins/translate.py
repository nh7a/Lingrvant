# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import re
import urllib
from lingrvant import Plugin
from demjson import decode as decode_json


class Translate(Plugin):
    """Google translate Plugin for Lingrvant"""

    def help(self):
        """Help"""
        return """!T from|to text...
!T |to text...
Supported languages: Albanian, Arabic, Bulgarian, Chinese (Simplified and Traditional), Catalan, Croatian, Czech, Danish, Dutch, English, Estonian, Filipino, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Latvian, Lithuanian, Maltese, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Serbian, Slovak, Slovenian, Swedish, Thai, Turkish, Ukrainian, Vietnamese"""

    def cmd_T(self, argv):
        """Translate query"""
        if argv == None or len(argv) < 2:
            return

        langpair = argv[0]
        query = ' '.join(argv[1:])
        params = {'v': '1.0', 'langpair':langpair, 'q': self.utf8_str(query)}
        url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
        params = urllib.urlencode(params)
        f = urllib.urlopen(url + params)
        res = decode_json(f.read())
        if res['responseData']:
            return res['responseData']['translatedText']
        return res['responseDetails']


Plugin.register(Translate())
