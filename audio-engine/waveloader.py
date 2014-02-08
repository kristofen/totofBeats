from scipy.io import wavfile
from scipy import fft
import numpy as np

class WaveLoader(object):
    """Waveloader"""

    def __init__(self, file):
        self.file = file

    def open(self):
        self.sRate, self.data = wavfile.read(self.file) #load wave file (sRate = sampleRate, data =content)
        self.nbSamples = self.data.shape[0] #nb samples for each channel
        self.index = 0 # init ptr
        self.indexinv = self.nbSamples-1 # init ptr inverse
        self.sType = self.data.dtype # original type
        self.sWidth = self.data.dtype.itemsize #original sample size
        #self.nbChannel = self.data.ndim
        self.nbChannel = 1 #nb of channel
        if self.data.ndim>1:
            self.nbChannel=self.data.shape[1]
        self.speed = 1.0 # speed (optional)
        self.data = (2. * self.data.astype(np.float32)) / float(2**(self.sWidth*8)) # convert audio from intnn to float
        self.dataInv = self.data[::-1] # inverse view of data (do this after conversion; see above)

class FakeWaveLoader(object):
    """FakeWaveloader"""

    def __init__(self, file):
        self.file = file

    def open(self):
        # SIN
        self.sRate=44100.
        #self.data = np.ones((10000,2),dtype=np.float32)


        freq = 800 #Hz
        length = 0.4 # sec
        nbsamples = int(self.sRate*length)
        self.data = np.zeros((nbsamples,2),dtype=np.float32)
        self.data[:,0]=np.sin(np.linspace(0.,2.*np.pi*(freq*length),nbsamples))
        self.data[:,1]=np.cos(np.linspace(0.,2.*np.pi*(freq*length),nbsamples))

        self.nbSamples = self.data.shape[0] #nb samples for each channel
        self.index = 0 # init ptr
        self.indexinv = self.nbSamples-1 # init ptr inverse
        self.sType = self.data.dtype # original type
        self.sWidth = self.data.dtype.itemsize #original sample size
        #self.nbChannel = self.data.ndim
        self.nbChannel = 1 #nb of channel
        if self.data.ndim>1:
            self.nbChannel=self.data.shape[1]
        self.speed = 1.0 # speed (optional)
        #self.data = (2. * self.data.astype(np.float32)) / float(2**(self.sWidth*8)) # convert audio from intnn to float
        self.dataInv = self.data[::-1] # inverse view of data (do this after conversion; see above)

##        ###### ONES
##        self.sRate=44100.
##        self.data = np.ones((10000,2),dtype=np.float32)
##        self.nbSamples = self.data.shape[0] #nb samples for each channel
##        self.index = 0 # init ptr
##        self.indexinv = self.nbSamples-1 # init ptr inverse
##        self.sType = self.data.dtype # original type
##        self.sWidth = self.data.dtype.itemsize #original sample size
##        #self.nbChannel = self.data.ndim
##        self.nbChannel = 1 #nb of channel
##        if self.data.ndim>1:
##            self.nbChannel=self.data.shape[1]
##        self.speed = 1.0 # speed (optional)
##        #self.data = (2. * self.data.astype(np.float32)) / float(2**(self.sWidth*8)) # convert audio from intnn to float
##        self.dataInv = self.data[::-1] # inverse view of data (do this after conversion; see above)


##        self.sRate, self.data = wavfile.read(self.file) #load wave file (sRate = sampleRate, data =content)
##        self.nbSamples = self.data.shape[0] #nb samples for each channel
##        self.index = 0 # init ptr
##        self.indexinv = self.nbSamples-1 # init ptr inverse
##        self.sType = self.data.dtype # original type
##        self.sWidth = self.data.dtype.itemsize #original sample size
##        #self.nbChannel = self.data.ndim
##        self.nbChannel = 1 #nb of channel
##        if self.data.ndim>1:
##            self.nbChannel=self.data.shape[1]
##        self.speed = 1.0 # speed (optional)
##        self.data = (2. * self.data.astype(np.float32)) / float(2**(self.sWidth*8)) # convert audio from intnn to float
##        self.dataInv = self.data[::-1] # inverse view of data (do this after conversion; see above)
