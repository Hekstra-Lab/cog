import pandas as pd
import cPickle as pickle

class DataSet():
    """
    Laue crystallography dataset for processing in Precognition.

    Provides a set of attributes and methods that can be used for 
    representing and analyzing Laue diffraction experiments.
    """

    def __init__(self, frames):
        self.frames = frames
        
    @property
    def frames(self):
        return self.__frames

    @frames.setter
    def frames(self, frames):
        self.__frames = frames

    def toPickle(self, pklfile="DataSet.pkl"):
        with open(pklfile, 'wb') as pkl:
            pickle.dump(self, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        return
        
    def fromPickle(self, pklfile):
        with open(pklfile, "rb") as pkl:
            self = pickle.load(pkl)
        return self
