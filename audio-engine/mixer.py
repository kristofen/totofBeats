#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Christophe
#
# Created:     25/01/2014
# Copyright:   (c) Christophe 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pyaudio
import numpy as np


class Mixer(object):
    """Mixer """
    # output parameters
    sRate = 44100   # sample rate
    #sWidth = 2      # largeur d'un sample en octets
    nbChannel = 2   # nb canaux
    p = None            # PyAudio instance
    stream = None       # PyAudio stream
    generator = None


    @staticmethod
    def start():
        Mixer.p = pyaudio.PyAudio()
        Mixer.stream = Mixer.p.open(format=pyaudio.paFloat32,
                channels=Mixer.nbChannel,
                rate=Mixer.sRate,
                output=True,
                stream_callback=Mixer.audioCallback)
        Mixer.stream.start_stream()

    @staticmethod
    def stop():
        Mixer.stream.stop_stream()
        Mixer.stream.close()
        Mixer.p.terminate()

    @staticmethod
    def registerGenerator(generator):
        Mixer.generator = generator

    @staticmethod
    def NeedSamples(nb,time):
        #ask tracks nb samples
        # and mix it
        if (Mixer.generator is not None):
            tmp = Mixer.generator.needSamples(nb,time)
        else:
            if Mixer.nbChannel>1:
                tmp = np.zeros(nb*2,dtype=np.float32).reshape((nb,2))
            else:
                tmp = np.zeros(nb,dtype=np.float32)

        data = (tmp).tostring()
        return data

    @staticmethod
    def audioCallback(in_data, frame_count, time_info, status):
        ret = pyaudio.paContinue
        #print "need"
        data = Mixer.NeedSamples(frame_count,time_info)
        return (data, ret)

