import numpy as np
import math

class Heights:

    def getHeights(M,facesID):
        faces_nodesID = M.faces.connectivities[facesID[:]] #return the nodes global ID
        volume_center_coords = M.volumes.center(M.volumes())
        adjacents_volumesID = M.faces.bridge_adjacencies(facesID[:],2,3)
        n = M.faces.normal[facesID]


        face_nodes_coords = M.nodes.coords[faces_nodesID[:,0]] #one is enough
        d = -(n*face_nodes_coords).sum(axis=1)#(n[:,0]*face_nodes_coords[:,0]+n[:,1]*face_nodes_coords[:,1]+n[:,2]*face_nodes_coords[:,2])
        coords_vol = volume_center_coords[adjacents_volumesID[:,:]]
        nn = np.zeros(coords_vol.shape)

        if len(adjacents_volumesID[0])>1:
            nn[:,0,:] = n
            nn[:,1,:] = n
            dd = np.zeros((len(facesID),2))
            dd[:,0] = d
            dd[:,1] = d
            aa = np.zeros((len(facesID),2))
            aa[:,0] = ((n*n).sum(axis=1))**(1/2)
            aa[:,1] = ((n*n).sum(axis=1))**(1/2)

            heights = abs((nn*coords_vol).sum(axis=2)+dd)/aa

        else:
            nn[:,0,:] = n
            dd = np.zeros((len(facesID),1))
            dd[:,0] = d
            aa = np.zeros((len(facesID),1))
            aa[:,0] = ((n*n).sum(axis=1))**(1/2)
            heights = abs((nn*coords_vol).sum(axis=2)+dd)/aa

        return heights

    def compute_heights(self):
        M = self.mesh #just in case self.mesh starts to call self.M for example
        internal_facesID = M.faces.internal[:]
        boundary_facesID = M.faces.boundary[:]
        internal_heights = Heights.getHeights(M,internal_facesID)
        boundary_heights = Heights.getHeights(M,boundary_facesID)
        return boundary_heights, internal_heights
#a*coords_vol[:,0]+b*coords_vol[:,1]+c*coords_vol[:,2]
