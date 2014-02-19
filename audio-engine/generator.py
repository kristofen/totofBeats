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
import math
import thread
import threading

# Generator: container for audio tracks to play
class Generator(object):
    """Generator"""

    trace=False # for debug
    counter=0   # for debug

    def __init__(self,sampleRate,nbChannels,nbTracks):
        # constructor
        self.library = Library('C:\\Users\\Christophe\\Documents\\Drum Samples\\')
        self.isOn=True
        self.bpm = 120.
        self.ptr=int(0)
        self.ptrLock = threading.Lock()
        self.nbticks = 16 # number of ticks
        self.ticksperbeat = 4 # number of ticks per beat
        self.sampleRate = sampleRate # sample frequency
        self.nbChannels = nbChannels # nb output channel to generate
        self.tracks = [] # allocates array of tracks
        for i in range(nbTracks):
            wl=None
            if i==0:
                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Bassdrum-01.wav')
                wl.open()
            elif i==1:
                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Snaredrum.wav')
                wl.open()
            elif i==2:
                wl=WaveLoader('C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-808\\Hat Closed.wav')
                wl.open()

            if wl is not None:
                self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,wl,i)) # allocates each track individually
            else:
                self.tracks.append(GeneratorTrack(self.nbticks,self.ticksperbeat,self.bpm,None,i)) # allocates each track individually

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

class GeneratorTrack(object):
    """GeneratorTrack"""
#Generatortrack:

    def __init__(self,nbticks,ticksperbeat,bpm,wl,i):
        self.nbticks = nbticks  # total ticks on the track
        self.ticksperbeat=ticksperbeat # nb ticks per beat (<== not used ?)
        self.allocateTicks() # allocates ticks array
        self.bpm=bpm #curBpm
        self.wl = wl #references waveloader
        self.master=None # master track (is read directly from generator)
        self.i=i
##        if i==0:
##            self.changeTick(0,False)
####            self.changeTick(2,True)
####            self.changeTick(4,True)
####            self.changeTick(8,True)
####            self.changeTick(12,True)
##        elif i==1:
####            self.changeTick(0,False)
##            self.changeTick(0,False)
####            self.changeTick(4,True)
####            self.changeTick(8,False)
####            self.changeTick(12,True)
####            self.changeTick(15,True)
##        elif i==2:
####            self.changeTick(0,False)
##            self.changeTick(0,False)
####            self.changeTick(2,True)
####            self.changeTick(4,True)
####            self.changeTick(6,True)
####            self.changeTick(8,False)
####            self.changeTick(10,True)
####            self.changeTick(12,True)
####            self.changeTick(14,True)
##
        self.allocateBuffer()
        self.refreshTrack()
        self.updateMaster()

    def allocateTicks(self):
        # creates array of ticks
        self.ticks = np.zeros((self.nbticks,),dtype=np.bool) #init ticks (booleans true=> ticks on false => ticks off)

    def registerWave(self,wl):
        self.wl=wl
        self.allocateBuffer
        self.refreshTrack
        self.updateMaster

    def changeBpm(self,bpm):
        #changes bpm of track
        self.bpm=bpm

    def changeTick(self,index,value):
        #set value of a tick of the track
        #value must be bool
        self.ticks[index]=value
        print self.ticks
        self.allocateBuffer()
        self.refreshTrack()
        self.updateMaster()

    @staticmethod
    def getBufferDepth(pNbTicks,pTpb,pBpm,pSRate):
        nbbeats = int(pNbTicks/pTpb) # nb of beats
        nbseconds = (60./pBpm)*float(nbbeats) # nb of seconds (float) to generate
        f,ret = math.modf(nbseconds*float(pSRate)) # gets integer part (bufferdepth) and decimal part (f) of total samples of track
        # if nb samples is closer to ceiling than floor then increment nb samples
        if f>0.5:
            ret+=1
        return int(ret)

    def allocateBuffer(self):
        # allocates buffer (unit samples) according of
        #  nbticks (total ticks of track)
        #  ticksperbeat
        #  bpm
        # sets BufferDepth in samples
        self.bufferdepth=GeneratorTrack.getBufferDepth(self.nbticks,self.ticksperbeat, self.bpm, Mixer.sRate)

        # allocates buffer according to nb channels
        if Mixer.nbChannel==1:
            self.buffer = np.zeros(self.bufferdepth,dtype=np.float32)
        else:
            self.buffer = np.zeros(Mixer.nbChannel*self.bufferdepth,dtype=np.float32).reshape((self.bufferdepth,Mixer.nbChannel))

    def refreshTrack(self):
        # edits buffer according to selected ticks
        indexes= np.nonzero(self.ticks)[0] # gets indexes of ticks activated
        if len(indexes)>0 and (self.wl is not None) :
            for i in indexes:
                # gets pointer of current ticks in sample unit
                ptr=math.floor(i*(self.bufferdepth/self.nbticks)) # index*nb samples per ticks
                len2move=min(self.buffer.shape[0]-ptr,self.wl.nbSamples) # length of wave file to move (crop if longer than remaining buffer)
                self.buffer[ptr:ptr+len2move,:]+=self.wl.data[0:len2move,:] # move it
                if self.wl.nbSamples>len2move: # if wave file is longer than  len moved then we move remaining wave samples at the beginning of buffer
                    self.buffer[0:self.wl.nbSamples-len2move,:]+=self.wl.data[len2move:,:]

    def updateMaster(self):
        # copies work buffer in the master track
##        print "i=",self.i," update master with min=",np.min(self.buffer)," max=",np.max(self.buffer)
        self.master=np.copy(self.buffer)


    def needSample(self,nbsamples,ptr):
        # returns nbsamples from master
        if self.master is None:
            return None
        else:
            ret = None
            if (ptr+nbsamples)>self.bufferdepth:
                # must copy end and begin of buffer
                a1=self.master[ptr:self.master.shape[0],:]  # first part (end of buffer)
                a2=self.master[0:nbsamples-(self.master.shape[0]-ptr),:] # second part (begin buffer)
                ret = np.vstack((a1,a2)) # returns concatenation of both parts
                #self.ptr = nbsamples-(self.master.shape[0]-self.ptr) # updates pointer
            else:
                # one copy in sufficient
                ret = self.master[ptr:ptr+nbsamples,:]
                #self.ptr += nbsamples
##            if np.max(ret)>1.:
##                print "[",self.i,"] over 1.0 retmax=",np.max(ret)," mastermax=",np.max(self.master), "buffermax=",np.max(self.buffer)
            return np.copy(ret)

##    def needSample(self,nbsamples):
##        # returns nbsamples from master
##        if self.master is None:
##            return None
##        else:
##            ret = None
##            if (self.ptr+nbsamples)>self.bufferdepth:
##                # must copy end and begin of buffer
##                a1=self.master[self.ptr:self.master.shape[0],:]  # first part (end of buffer)
##                a2=self.master[0:nbsamples-(self.master.shape[0]-self.ptr),:] # second part (begin buffer)
##                ret = np.vstack((a1,a2)) # returns concatenation of both parts
##                self.ptr = nbsamples-(self.master.shape[0]-self.ptr) # updates pointer
##            else:
##                # one copy in sufficient
##                ret = self.master[self.ptr:self.ptr+nbsamples,:]
##                self.ptr += nbsamples
##            return ret