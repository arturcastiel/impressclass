import numpy as np
import pdb

def k_eq_dep0(hb, hi, all_faces, internal_faces, b_faces, u_normal, adjacencies_internal_faces, adjacencies_boundary_faces, perms):
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

    for i, f in enumerate(internal_faces):
        k0 = perms[adjacencies_internal_faces[i][0]].reshape([3, 3])
        k1 = perms[adjacencies_internal_faces[i][1]].reshape([3, 3])
        unit_normal = u_normal[f]
        k0 = np.dot(np.dot(k0, unit_normal), unit_normal)
        k1 = np.dot(np.dot(k1, unit_normal), unit_normal)
        h0 = hi[i][0]
        h1 = hi[i][1]
        k = (h0 + h1)/(k0/h0 + k1/h1)
        keq[f] = k

    for i, f in enumerate(b_faces):
        k0 = perms[adjacencies_boundary_faces[i][0]].reshape([3, 3])
        unit_normal = u_normal[f]
        k0 = np.dot(np.dot(k0, unit_normal), unit_normal)
        keq[f] = k0

    return keq

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
    k0 = perms

    kf0 = (k0[:, 0, :]*unit_vectors).sum(axis=1)
    kf1 = (k0[:, 1, :]*unit_vectors).sum(axis=1)
    kf2 = (k0[:, 2, :]*unit_vectors).sum(axis=1)
    return (np.array([kf0, kf1, kf2]).T*unit_vectors).sum(axis=1)
