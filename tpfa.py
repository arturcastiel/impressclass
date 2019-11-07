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

    def getHeights(self,facesID):
        faces_nodesID = self.mesh.faces.connectivities[facesID[:]] #return the nodes global ID
        adjacents_volumesID = self.mesh.faces.bridge_adjacencies(facesID[:],2,3)
        volume_center_coords = self.mesh.volumes.center(M.volumes())
        adjacents_volumes_coords = volume_center_coords[adjacents_volumesID[:,:]]

        normal_vector = self.mesh.faces.normal[facesID]
        normal_vector_modulus = np.linalg.norm(normal_vector,axis=1)
        face_node_coords = self.mesh.nodes.coords[faces_nodesID[:,0]] #one is enough
        d_coefficient = -(normal_vector*face_node_coords).sum(axis=1) # from the plane equation (a*x+b*y+c*z+d = 0)

        normal_vector_reshape = normal_vector[:,np.newaxis,:]
        d_coefficient_reshape = d_coefficient[:,np.newaxis]
        normal_vector_modulus_reshape = normal_vector_modulus[:,np.newaxis]

        heights = abs((normal_vector_reshape*adjacents_volumes_coords).sum(axis=2)+d_coefficient_reshape)/normal_vector_modulus_reshape
        return heights

    def compute_heights(self):
        internal_facesID = self.mesh.faces.internal[:]
        boundary_facesID = self.mesh.faces.boundary[:]
        internal_heights = self.getHeights(internal_facesID)
        boundary_heights = self.getHeights(boundary_facesID)
        return boundary_heights, internal_heights

    def compute_eq_permeability(self):
        ''' compute equivalent permeability project on each
            face of the domain '''
        return k_eq

    def assembly_tpfa(self):

        return T,Q
