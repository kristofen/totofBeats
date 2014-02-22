

###-------------------------------------------------------------------------------
### Name:        Configuration Manager
### Purpose:     Loads and Saves Xml config files
###
### Author:      Christophe
###
### Created:     22/02/2014
### Copyright:   (c) Christophe 2014
### Licence:     <your licence>
###-------------------------------------------------------------------------------
##
##import xml.etree.ElementTree as et
##
##class ConfigurationManager(object):
##    """ConfigurationManager"""
##
##    def __init__(self,confFile):
##        self.confFile=confFile
##        self.loadXml()
##
##    def loadXml(self):
##        # will load parameters from xml File
##        self.resetConf()
##        tree = et.parse(self.confFile)
##        root = tree.getroot()
##        kits = root.find('kits')
##        for kit in kits.findall('kit'):
##            print "kitName=",kit.get('name')
##            for track in kig.findall('track'):
##                print "  track ",track.get('index'),track.get('file'),track.get('gain')
##        library = root.find('library')
##        print "library path=",library.get('folder')
##
##
##    def saveXml(self):
##        # will save parameters to xml file
##        dummy=""
##
##    def resetConf(self):
##        # must reset conf
##        dummy=""
