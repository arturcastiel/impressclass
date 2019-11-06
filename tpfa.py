import numpy as np
import pdb

class tpfaScheme(object):
    def __init__(self, mesh):
        self.mesh = mesh
        # self.hb, self.hi = self.compute_heights()
        # self.k_eq = self.compute_eq_permeability()

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

        M = self.mesh
        hi = self.hi
        hb = self.hb
        all_faces = M.faces.all
        internal_faces = M.faces.internal
        b_faces = M.faces.boundary
        u_normal = M.faces.normal[all_faces]
        adjacencies_internal_faces = M.faces.bridge_adjacencies(internal_faces, 2, 3)
        adjacencies_boundary_faces = M.faces.bridge_adjacencies(b_faces, 2, 3)
        perms = M.permeability[:]
        from tpfa_functions.eq_permeability import k_eq

        return k_eq(hb, hi, all_faces, internal_faces, b_faces, u_normal, adjacencies_internal_faces, adjacencies_boundary_faces, perms)

    def assembly_tpfa(self):

        return T,Q

if __name__ == '__main__':
    from impress.preprocessor.meshHandle.finescaleMesh import FineScaleMesh as msh
    import timeit

    name_mesh = 'mesh/27x27x27.msh'
    dim = 3
    M = msh(name_mesh, dim=dim)
    M.permeability[:] = [10., 0., 0., 0., 5.0, 0., 0., 0., 2]

    m1 = tpfaScheme(M)
    hi = np.ones([len(M.faces.internal), 2], dtype = np.float64)
    m1.hi = hi
    hb = np.ones([len(M.faces.boundary), 1], dtype=np.float64)
    m1.hb = hb
    keq = m1.compute_eq_permeability()

    pdb.set_trace()
