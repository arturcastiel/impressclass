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

        all_faces = self.mesh.faces.all
        internal_faces = self.mesh.faces.internal
        b_faces = self.mesh.faces.boundary
        u_normal = np.absolute(self.mesh.faces.normal[all_faces])
        adjacencies_internal_faces = self.mesh.faces.bridge_adjacencies(internal_faces, 2, 3)
        adjacencies_boundary_faces = self.mesh.faces.bridge_adjacencies(b_faces, 2, 3)
        perms = self.mesh.permeability[:]

        keq = np.zeros(len(all_faces))

        k00 = self.get_perm_proj(perms[adjacencies_internal_faces[:, 0]].reshape([len(internal_faces), 3, 3]), u_normal[internal_faces])
        k11 = self.get_perm_proj(perms[adjacencies_internal_faces[:, 1]].reshape([len(internal_faces), 3, 3]), u_normal[internal_faces])
        keq[internal_faces] = self.hi.sum(axis=1)/(self.hi[:, 0]/k00 + self.hi[:, 1]/k11)

        keq[b_faces] = self.get_perm_proj(perms[adjacencies_boundary_faces.flatten()].reshape([len(b_faces), 3, 3]), u_normal[b_faces])

        return keq

    def get_perm_proj(self, perms, unit_vectors):
        '''
        obtem a permeabilidade projetada na face
        input:
            perms: permeabilidade dos volumes
            unit_vectors: vetor normal unitario das faces
        output:
            permeabilidade projetada
        '''

        tt = perms*unit_vectors.reshape([len(unit_vectors), 1, 3])
        return tt.sum(axis=2).sum(axis=1)

    def assembly_tpfa(self):

        return T,Q
