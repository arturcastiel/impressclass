import numpy as np
import pdb

def k_eq(hb, hi, all_faces, internal_faces, b_faces, u_normal, adjacencies_internal_faces, adjacencies_boundary_faces, perms):
    '''
    calcula a permeabilidade equivalente das faces

    input:
        hb: altura das faces do contorno
        hi: altura das faces internas
        all_faces: ids de todas as faces
        internal_faces: ids das faces internas
        b_faces: boundary faces
        u_normal: vetor normal unitario de all_faces
        adjacencies_faces: volumes vizinhos de all_faces
        perms: permeabilidade de todos os volumes
        all_volumes: ids de todos os volumes

    output:
        keq: permeabilidade equivalente de all_faces
    '''

    keq = np.zeros(len(all_faces))

    ids0 = adjacencies_internal_faces[:, 0]
    ids1 = adjacencies_internal_faces[:, 1]
    unit_normal_internal_faces = np.absolute(u_normal[internal_faces])

    ni = len(internal_faces)
    k00 = get_perm_proj(perms[ids0].reshape([ni, 3, 3]), unit_normal_internal_faces)
    k11 = get_perm_proj(perms[ids1].reshape([ni, 3, 3]), unit_normal_internal_faces)
    keq[internal_faces] = hi.sum(axis=1)/(hi[:, 0]/k00 + hi[:, 1]/k11)

    idsb = adjacencies_boundary_faces.flatten()
    unit_normal_b_faces = np.absolute(u_normal[b_faces])
    nb = len(b_faces)
    keq[b_faces] = get_perm_proj(perms[idsb].reshape([nb, 3, 3]), unit_normal_b_faces)

    return keq

def get_perm_proj(perms, unit_vectors):
    '''
    obtem a permeabilidade projetada na face
    input:
        perms: permeabilidade dos volumes
        unit_vectors: vetor normal unitario das faces
    output:
        permeabilidade projetada

    '''

    tt = np.zeros(perms.shape)
    tt[:, 0, :] = unit_vectors
    tt[:, 1, :] = unit_vectors
    tt[:, 2, :] = unit_vectors
    tt = perms*tt
    return tt.sum(axis=2).sum(axis=1)
