#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Christophe
#
# Created:     31/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from scipy.io import wavfile
import numpy as np
import pyaudio
import time
from simpleptr import *

def audioCallback(in_data, frame_count, time_info, status):
    if SimplePtr.counter<5:
        print time_info
    SimplePtr.counter += 1
    ret = pyaudio.paContinue
    #print "need"
    #data = Mixer.NeedSamples(frame_count)
    data = (SimplePtr.d[SimplePtr.ptr:SimplePtr.ptr+frame_count,:]).tostring()
    SimplePtr.ptr += frame_count
    return (data, ret)

def main():

##    file = 'C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-909\\Bassdrum-01.wav'
    file = 'C:\\Users\\Christophe\\Documents\\Samples\\04 - HARDER, BETTER, FASTER, STRONGER.wav'
##    file = 'C:\\Users\\Christophe\\Documents\\Drum Samples\\Roland TR-909\\Bassdrum-01-mono.wav'
##    file = 'C:\\Users\\Christophe\\Documents\\Drum Samples\\test6channels\\6_Channel_ID.wav'
    sRate, SimplePtr.d = wavfile.read(file)   # read file
    nbSamples = SimplePtr.d.shape[0]          # get nb samples
    sType = SimplePtr.d.dtype                 # get type of samples
    sWidth = SimplePtr.d.dtype.itemsize       # get size of each sample
    nbChannel = 1             # number of channels
    if SimplePtr.d.ndim>1:
        nbChannel=SimplePtr.d.shape[1]

    print "sRate=",sRate," nbSamples=",nbSamples," sType=",sType," sWidth=",sWidth," nbChannels=",nbChannel

    print "min=",np.min(SimplePtr.d)," max=",np.max(SimplePtr.d)
    SimplePtr.d = (2. * SimplePtr.d.astype(np.float32)) / float(2**(sWidth*8))
    print "min=",np.min(SimplePtr.d)," max=",np.max(SimplePtr.d)

    SimplePtr.ptr=0

    p = pyaudio.PyAudio()
    stream = p.open(format= pyaudio.paFloat32,
        channels=nbChannel,
        rate=sRate,
        output=True,
        stream_callback=audioCallback)

##    stream = p.open(format=p.get_format_from_width(sWidth),
##        channels=nbChannel,
##        rate=sRate,
##        output=True,
##        stream_callback=audioCallback)
    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()

    pass

if __name__ == '__main__':

    main()
