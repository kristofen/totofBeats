import numpy as np
from mixer import *
from waveloader import *
from library import *
import math
import thread
import threading

class GeneratorTrack(object):
    """GeneratorTrack"""
#Generatortrack:

    def __init__(self,nbticks,ticksperbeat,bpm,wl,i,label,gain):
        self.label=label
        self.gain=gain
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
                wlNbSample=min(self.buffer.shape[0],self.wl.nbSamples) # if wave is longer than grid then takes only grid length
                len2move=min(self.buffer.shape[0]-ptr,wlNbSample) # length of wave file to move (crop if longer than remaining buffer)
                self.buffer[ptr:ptr+len2move,:]+=self.wl.data[0:len2move,:] # move it
                if wlNbSample>len2move: # if wave file is longer than  len moved then we move remaining wave samples at the beginning of buffer
                    self.buffer[0:wlNbSample-len2move,:]+=self.wl.data[len2move:wlNbSample,:]

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