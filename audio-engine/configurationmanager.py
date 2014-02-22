#-------------------------------------------------------------------------------
# Name:        Configuration Manager
# Purpose:     Loads and Saves Xml config files
#
# Author:      Christophe
#
# Created:     22/02/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json

class ConfigurationManager(object):
    """ConfigurationManager"""

    def __init__(self,confFile):
        self.confFile=confFile
        self.load()
        self.conf=None

    def load(self):
        # will load parameters from xml File
        self.resetConf()
        f = open(self.confFile).read()
        obj=json.loads(f)
        self.conf=obj[0]
##        print "Conf loaded=",self.conf

    def save(self):
        # will save parameters to xml file
        open(self.confFile,'w').write('['+json.dumps(self.conf)+']')

    def resetConf(self):
        # must reset conf
        self.conf=None
