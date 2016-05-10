from __future__ import unicode_literals
import ConfigParser
import os
from django.conf import settings
import logging    

log = logging.getLogger(__name__)

COMMON_DIR = os.path.dirname(__file__)
COMMON_INI_PATH = os.path.join(COMMON_DIR, "common.ini")
Config = ConfigParser.ConfigParser()
Config.read(COMMON_INI_PATH)

def ConfigSectionMap(section):
    data = {}
    options = Config.options(section)
    for option in options:
        try:
            data[option] = Config.get(section, option)
            if data[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            data[option] = None
    return data