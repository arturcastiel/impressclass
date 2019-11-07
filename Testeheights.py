import numpy as np
from impress import FineScaleMeshMS as msh
from heights import compute_heights

class Testeheights(object):
    def __init__(self,M):
        self.mesh = M

    def run(self):
        hb,hi = compute_heights(self)
        return hb,hi

M = msh('20.h5m', dim = 3)
obj = Testeheights(M)
