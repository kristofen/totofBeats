#-------------------------------------------------------------------------------
# Name:        Generator(class)
# Purpose:
#
# Author:      Christophe
#
# Created:     30/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
from mixer import *
from waveloader import *
from library import *
from generatortrack import *
import math
import thread
import threading

# Generator: container for audio tracks to play
class Generator(object):
    """Generator"""

    trace=False # for debug
    counter=0   # for debug

    def __init__(self,sampleRate,nbChannels,confMan):
        # constructor
        self.library = Library(confMan.conf['library'])
        self.isOn=True
        self.bpm = 120.
        self.ptr=int(0)
        self.ptrLock = threading.Lock()
        self.nbticks = 16 # number of ticks
        self.ticksperbeat = 4 # number of ticks per beat
        self.sampleRate = sampleRate # sample frequency
        self.nbChannels = nbChannels # nb output channel to generate
        self.tracks = [] # allocates array of tracks
        self.confMan=confMan
        kit=confMan.conf['kits'][0]
        for i in range(len(kit['tracks'])):
            wl=None
            trk=kit['tracks'][i]
            if trk['file']!="":
                print trk['file']
                wl=WaveLoader(self.library.getPath(trk['file']))
                wl.open()

            if wl is not None:
                self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,wl,i,trk['name'],float(trk['gain']))) # allocates each track individually
            else:
                self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,None,i,trk['name'],float(trk['gain']))) # allocates each track individually

##        for i in range(nbTracks):
##            wl = None
##            if i==0:
####                wl=FakeWaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Snaredrum.wav')
##                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Bassdrum-01.wav')
##                wl.open()
##            elif i==1:
####                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Snaredrum.wav')
##                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Snaredrum.wav')
##                wl.open()
##            elif i==2:
####                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Snaredrum.wav')
##                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Hat Closed.wav')
##                wl.open()
##            if wl is not None:
##                self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,wl,i)) # allocates each track individually
        self.bufferdepth=GeneratorTrack.getBufferDepth(self.nbticks,self.ticksperbeat,self.bpm,self.sampleRate)

    def changeBpm(self,bpm):
        for i,value in enumerate(self.tracks):
            value.changeBpm(bpm)

    def needSamples(self,nbsamples,time):
        # function called by audio mixer,
        # this function may return the nb of sample desired

        if self.isOn==False:
            return None

        if Generator.trace==True:
            print "nbsamples=",nbsamples," ptr=",self.ptr," bufferdepth=",self.bufferdepth
        outp=None
        nb=0
        for i,v in enumerate(self.tracks):
            ret = v.needSample(nbsamples,self.ptr)

            if ret is not None:
                nb+=1
                if outp is None:
                    outp=ret
                else:
                    outp+=ret

        if nb>1:
            outp = outp/nb

        # UPDATE read ptr (must lock for eventual updates)
        try:
            self.ptrLock.acquire()
            if(self.ptr+nbsamples)>self.bufferdepth:
                self.ptr = nbsamples-(self.bufferdepth-self.ptr) # updates pointer
            else:
                self.ptr += nbsamples
        finally:
            self.ptrLock.release()

        return outp

## #######################################################
## Generator commands

    def start(self):
        if self.isOn==False:
            self.cue(0)
            self.isOn=True

    def stop(self):
        self.isOn=False

    def pause(self):
        self.isOn=False

    def cue(self,tickptr):
        # moves play pointer to tickPtr
        # tickptr is expressed in ticks unit. ie: in the interval [0,(nbbeats*ticksperbeats)-1]
        # !!! self.ptr is expressed in sample unit. So we need to convert tickptr
        with self.ptrLock:    # we lock while updating ptr
            self.ptr = int( float(self.bufferdepth) *  float(tickptr)/float(self.nbticks))

    def gridWidth(self,pBeats,pTicksPerBeat):
        # modifies grid width in ticks
        # pBeats (int) nb beats in the width
        # pTicksPerBeat (int) nb ticks per beat
        if self.isOn==False:
            self.nbticks = pBeats*pTicksPerBeat
            self.ticksperbeat = pTicksPerBeat
            for k,v in self.tracks:
                v.nbticks=self.nbticks #change number of ticks
                v.ticksperpbeat=self.ticksperbeat # change number of ticks per beat
                v.allocateTicks() # re-generate array of ticks (on/off)
                v.allocateBuffer() # re-allocate buffer of audio samples
                v.updateMaster()

    def gridHeight(self,nb):
        # args int nb of tracks to allocate
        if self.isOn==False:
            diff = nb - self.tracks
            if diff!=0:
                for i in range(abs(diff)):
                    if diff < 0:
                        self.tracks.pop()
                    elif diff >0:
                        self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,None,len(self.tracks)))

    def gridAddRow(self,pFile):
        if self.isOn==False:
            wl = None
            if pFile is not None:
                wl=WaveLoader(self.library.getPath(pFile))
                wl.open()
            self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,wl,len(self.tracks)))

    def gridRow(self,trackIndex,pFile):
        if trackIndex>=0 and trackIndex<len(self.tracks):
            wl=None
            if pFile is not None:
                wl=WaveLoader(self.library.getPath(pFile))
                wl.open()
            self.tracks[trackIndex].registerWave(wl)

    def gridCell(self,indexTrack,indexTick,tickState):
        ### tickState bool
        if indexTrack>=0 and indexTrack<len(self.tracks):
            self.tracks[indexTrack].changeTick(indexTick,tickState)


###========================================================================
###

