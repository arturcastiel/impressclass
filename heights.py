import numpy as np
import math

class Heights:
    def planeCoeff(nodes_coords):
        ''' Function created for compute the face plane equation coefficients
        Let a*x+b*y+c+d=0 be the plane equation, where:
          - a,b and c are the plane normal vector coordinates wich are computed
        as the vetorial product between two plane vectors
          - d can be computed as the negative of scalar product between the
        normal vector and a point "inside" the plane'''
        n = np.cross((nodes_coords[1] - nodes_coords[0]),\
                     (nodes_coords[2]-nodes_coords[0]))
        a,b,c = n
        d = -np.dot(n,nodes_coords[0])
        return a,b,c,d

    def getHeights(M,facesID):
        faces_nodesID = M.faces.connectivities[facesID[:]] #return the nodes global ID
        volume_center_coords = M.volumes.center(M.volumes())
        adjacents_volumesID = M.faces.bridge_adjacencies(facesID[:],2,3)

        if len(adjacents_volumesID[0])>1:
            coords_vol = np.zeros((2,3)); heights = np.zeros((len(facesID),2))
        else: coords_vol = np.zeros((1,3)); heights = np.zeros((len(facesID),1))

        for i in range(0,len(facesID)):
            face_nodes_coords = M.nodes.coords[faces_nodesID[i]]
            a,b,c,d = Heights.planeCoeff(face_nodes_coords)
            coords_vol[:,:] = volume_center_coords[adjacents_volumesID[i,:]]
            heights[i,:] = abs(a*coords_vol[:,0]+b*coords_vol[:,1]+c*coords_vol[:,2]+d)/(math.sqrt(a**2+b**2+c**2))

        return heights

    def heights(self):
        M = self.mesh #just in case self.mesh starts to call self.M for example
        internal_facesID = M.faces.internal[:]
        boundary_facesID = M.faces.boundary[:]
        internal_heights = Heights.getHeights(M,internal_facesID)
        boundary_heights = Heights.getHeights(M,boundary_facesID)
        return boundary_heights, internal_heights
