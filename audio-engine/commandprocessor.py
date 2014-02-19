#-------------------------------------------------------------------------------
# Name:        Command processor
# Purpose:     processes commands from bluetooth connection
#
# Author:      Christophe
#
# Created:     26/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class CommandProcessor(object):
    """CommandProcessor"""

    def __init__(self,generator):
        self.generator=generator
        self.buffer=""

    def registerClient(self,btc):
        self.btc=btc

    def bufferize(self,data):
        self.buffer += data
        print "CommandProcessor bufferize len(data)=",len(data)," len(buffer)=",len(self.buffer)
        mustStop=False
        ptrstart=0
        while (mustStop==False):
            index = self.buffer[ptrstart:].find('\r\n')
            if index!=-1:
                cmd=self.buffer[ptrstart:index]
                self.processCommand(cmd)
                ptrstart=index+2
            else:
                mustStop=True
        if ptrstart>0:
            print "CommandProcessor atleast one command processed will compress"
            self.buffer=self.buffer[ptrstart:]
            print "CommandProcessor after compress length=",len(self.buffer)


        #execute command and returns return code
    def processCommand(self,cmd):
        print "mustprocess command=",cmd
        response="error unknowncommand"
        index = cmd.find(' ')
        cmdKey=""
        cmdValue=""
        if index>0:
            cmdKey=cmd[0:index]
            cmdValue=cmd[index+1:]
        else:
            cmdKey=cmd

        if cmdKey=='corestart':
            response = self.cmdCoreStart(cmdValue)
        elif cmdKey=='corestop':
            response = self.cmdCoreStop(cmdValue)
        elif cmdKey=='corepause':
            response = self.cmdCorePause(cmdValue)
        elif cmdKey=='corecue':
            response = self.cmdCoreCue(cmdValue)
        elif cmdKey=='gridwidth':
            response = self.cmdGridWidth(cmdValue)
        elif cmdKey=='gridheight':
            response = self.cmdGridHeight(cmdValue)
        elif cmdKey=='gridaddrow':
            response = self.cmdGridAddRow(cmdValue)
        elif cmdKey=='gridrow':
            response = self.cmdGridRow(cmdValue)
        elif cmdKey=='gridcell':
            response = self.cmdGridCell(cmdValue)

        self.btc.sendCommand(response)

    def cmdCoreStart(self,arg):
        #starts the generator
        self.generator.start()
        return "ok"

    def cmdCoreStop(self,arg):
        #stops the generator (and sets pointer tick to 0)
        self.generator.stop()
        return "ok"

    def cmdCorePause(self,arg):
        #pauses generator (tick pointer stays the same)
        self.generator.pause()
        return "ok"

    def cmdCoreCue(self,arg):
        #sets tick pointer position (args 0 ==> sets pointer to the begining
        cueVal=int(arg)
        self.generator.cue(cueVal)
        return "ok"

    def cmdGridWidth(self,arg):
        #sets grid width with 2 arguments (nbbeats,number_of_ticks_per_beat)
        fields=arg.split(',')
        self.generator.gridWidth(int(fields[0]),int(fields[1])) # nbbeats,ticksperbeat
        return "ok"

    def cmdGridHeight(self,arg):
        #sets number of tracks to allocate (arg = nb tracks)
        self.generator.gridHeight(int(arg))
        return "ok"

    def cmdGridAddRow(self,arg):
        # adds one track to the grid (optional arg : filename of wav to play)
        self.generator.gridAddRow(arg)
        return "ok"

    def cmdGridRow(self,arg):
        # sets to already allocated track the wav to play
        fields=arg.split(',')
        self.generator.gridRow(int(fields[0]),fields[1]) # index track,track file
        return "ok"

    def cmdGridCell(self,arg):
        # enable/disable one tick (arg=indexrow,indextick,tick_state)
        # with tickstate 1=> tick activated
        #                0=> tick disabled
        f=arg.split(',') # indexrow, indextick, value on or off
        self.generator.gridCell(int(f[0]),int(f[1]),bool(int(f[2])))
        return "ok"


