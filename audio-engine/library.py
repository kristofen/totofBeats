#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Christophe
#
# Created:     10/02/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Library(object):
    """ """

    def __init__(self,path):
        self.path=path

    def getPath(self,pFile):
        return self.path+pFile