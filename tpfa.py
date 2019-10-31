import numpy as np

class tpfaScheme(object):
    def __init__(self, mesh):
        self.mesh = mesh
        self.hb, self.hi = self.compute_heights()
        self.k_eq = self.compute_eq_permeability()

    def __call__(self):
        self.run()
        pass

    def run(self):
        self.T, self.Q = self.assembly_tpfa()

    def compute_heights(self):
        #compute compute_heights
        return boundary_heights, internal_heights

    def compute_eq_permeability(self):
        ''' compute equivalent permeability project on each
            face of the domain '''
        return k_eq

    def assembly_tpfa(self):

        return T,Q
