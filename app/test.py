#!/usr/bin/env python
# Copyright (c) 2009 Naoki Hiroshima
# You can redistribute this and/or modify this under the same terms as Python.

import os, sys, logging
from lingrvant import Plugin

APP_DIRECTORY = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(APP_DIRECTORY, 'third_party'))

def readline():
    sys.stdout.write(">>> ")
    line = sys.stdin.readline()
    return line.strip()

def main():
    logging.basicConfig(level=logging.DEBUG)
    Plugin.load()

    line = readline()
    while line:
        for plugin in Plugin.plugins:
            response = plugin.on_message({'text':line})
            if response:
                print(response)
        line = readline()

if __name__ == '__main__':
    main()
