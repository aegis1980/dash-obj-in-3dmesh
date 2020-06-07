"""

"""
#built in modules

import math
from typing import List

#3rd party
import numpy as np

def split_quad(quad_face : List[int], vertices : List[List[float]],split_method = 0) -> List[int]:
    """
    converts quad face to 2No tri faces (as size-6 list of vertice refs)
    split method:
        0 (default) : min angle
        1 : max angle
        2 : shortest distance

    Args:
        quad_face : list of ints describing vertex ref of four corners of quad to be split
        vertices: obj file vertices    	
        split_method : approach used to split quad 
    """

    #quad vertices
    v0 = np.array(vertices[int(quad_face[0])])
    v1 = np.array(vertices[int(quad_face[1])])
    v2 = np.array(vertices[int(quad_face[2])])
    v3 = np.array(vertices[int(quad_face[3])])

    #quad edge vectors
    e0 = v1 - v0
    e1 = v2 - v1
    e2 = v3 - v2
    e3 = v0 - v3

    #option 1 split - edge from v2 to v4
    n1a = norm(np.cross(e0,-e3))
    n1b = norm(np.cross(-e1, e2))
    a1 = math.acos(np.dot(n1a, n1b))

    #option 2 split - edge v1 to v3
    n2a = norm(np.cross(e1,-e0))
    n2b = norm(np.cross(-e2, e3))
    a2 = math.acos(np.dot(n2a, n2b))

    if (abs(a1)>=abs(a2)):
        return [quad_face[0],quad_face[1],quad_face[3]] + [quad_face[1],quad_face[2],quad_face[3]]
    else:
        return [quad_face[0],quad_face[1],quad_face[2]] + [quad_face[2],quad_face[3],quad_face[0]]



def norm(a : np.array):
    """
    normalise 3d (np.)array
    """
    l  = math.sqrt(a[0]**2+a[1]**2+a[2]**2)
    return np.array([a[0]/l,a[1]/l,a[2]/l])