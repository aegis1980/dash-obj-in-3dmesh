# built-in py modules
from typing import List, Iterator
import os

# 3rd party modules
import numpy as np

# Local modules
import _config 
from mesh_tools import split_quad

class WavObject():
    """
    Parse 1 or many objects in wavefront obj file using one or other of static methof:
        WavObject.read_objfile(...)
    """

    COMMENT_LINE = '#' #this and everything else except the above is currently ignored.

    VERTEX_LINE = 'v '
    FACE_LINE = 'f '
    OBJECT_NAME_LINE = 'o '
    MATERIAL_LIB_LINE = 'mtllib '
    USE_MATERIAL_LINE = 'usemtl '

    def __init__(self):
        self.name : str = None 
        self.vertices  = []
        self.vertice_colors = []
        self.faces = []
        self.face_mtls: List(str) = []
        self.face_colors: List(List(int)) = []
        self.opacities: List(float) = []

    
    @staticmethod
    def _read_objfile(full_obj_filepath : str, split : bool = True):
        """
        Parses a wavefront obj file.
    
        Args:
            full_obj_filepath: full os-specific filepath of .obj file (e.g. ../../monkey.obj)
            split: if True then returns all objects in file as separate elements
        Returns: 
            my_objects : List of WavObjects
        """
        my_objects = [] # can be multiple sub objects in file,if split = True


        def triangulate_polygons(list_vertex_indices):
            for k in range(0, len(list_vertex_indices), 3):
                yield list_vertex_indices[k : k + 3]


        def process_faces(current_obj,face_mtls,index_correction, correction = 1):
            """
            correction = 1 for dash. 
            """

            current_obj.vertices = np.array(current_obj.vertices)
            current_obj.vertice_colors = np.array(current_obj.vertice_colors)
            current_obj.faces = [int(i) for i in current_obj.faces]
            current_obj.faces = np.array(list(triangulate_polygons(current_obj.faces))) - (correction + index_correction- (0 if len(my_objects) == 0 else 1))
            
            # currently we discard everything except the kd (diffuse color) 
            current_obj.face_colors = list(map(lambda x : x.kd,face_mtls))
            current_obj.opacities = list(map(lambda x : 1-x.tr,face_mtls))
            my_objects.append(current_obj)


        obj_mtls = {}
        vtx_indices = []

        # face_mtls this is just a temp array that is 'processed' in process_faces function
        # then cleared for next object
        face_mtls = [] 
        current_mtl = _BasicWavMaterial()
        with open(full_obj_filepath) as fp:
            index_correction = 0

            count=0 # running count of vertices in whole file
            prev_good_line = WavObject.VERTEX_LINE 
            current_obj = WavObject() # first object
            for i, line in enumerate(fp):
                
                if line.startswith(WavObject.VERTEX_LINE):
                    count = count+1
                    if prev_good_line == WavObject.FACE_LINE and split:
                        # new mesh object in file
                        # process & push current one into our my_objects list
                        process_faces(current_obj,face_mtls,index_correction)
                        
                        index_correction = count
                        #and start again
                        current_obj = WavObject()
                        face_mtls = []

                    line = line[2:].strip() # remove v and whitespace
                    # extract vertice color if more than 3 values.
                    if len(line.split()) > 3:
                        current_obj.vertices.append(
                            list(map(float, line.split()[:3])))
                        current_obj.vertice_colors.append(
                            list(map(float, line.split()[3:])))
                    else:
                        current_obj.vertices.append(list(map(float, line.split())))
                    prev_good_line = WavObject.VERTEX_LINE
                elif line.startswith(WavObject.FACE_LINE):
                    line = line[len(WavObject.FACE_LINE):].strip()
                    vtx_indices = [x.split('/')[0] for x in line.split()]
                    if len(vtx_indices) != 3:
                        # split quad face into two tris
                        vtx_indices = split_quad(vtx_indices,current_obj.vertices)
                        face_mtls.append(current_mtl)
                        
                    face_mtls.append(current_mtl)
                    current_obj.faces.extend(vtx_indices)
                    prev_good_line = WavObject.FACE_LINE
                elif line.startswith(WavObject.OBJECT_NAME_LINE):
                    line = line[len(WavObject.OBJECT_NAME_LINE):].strip()
                    current_obj.name = line
                    #todo this is a bit crude. Might not work 100% of the time. 
                elif line.startswith(WavObject.MATERIAL_LIB_LINE):
                    mtl_file = line[len(WavObject.MATERIAL_LIB_LINE):].strip() # remove mtllib and whitespace
                    dirname = os.path.dirname(full_obj_filepath)
                    full_mtl_filepath = os.path.join(dirname,mtl_file)
                    obj_mtls.update(_BasicWavMaterial.read_mtlfile(full_mtl_filepath))
                elif line.startswith(WavObject.USE_MATERIAL_LINE):
                    mtl_name = line[len(WavObject.USE_MATERIAL_LINE):].strip() # remove usemtl and whitespace
                    if mtl_name in obj_mtls:
                        current_mtl = obj_mtls[mtl_name]

        process_faces(current_obj,face_mtls, index_correction) # add last object (or only object!)
        return my_objects


    @staticmethod
    def read_objfile(component_name : str, obj_dir : str = _config.GEOMETRY_DIR, split = True):
        """
        public helper function.
        forms correct path and passes to _read_objfile()

        Args:
            component_name : obj file name without extension (without .obj or .mtl)

        """
        full_filepath = os.path.join(_config.DATA_PATH,obj_dir,component_name + ".obj")

        return WavObject._read_objfile(full_filepath,split)




###############################################################################################################

class _BasicWavMaterial:
    """
    Basic material 
    https://en.wikipedia.org/wiki/Wavefront_.obj_file#Basic_materials
    """

    NEW_MATERIAL = "newmtl "
    AMBIENT_COLOR = "Ka " # e.g. 1.000 1.000 1.000   is white
    DIFFUSE_COLOR = "Kd "
    SPECULAR_COLOR = "Ks "
    TRANSPARENCY = "Tr "
    DISSOLVE = "d "
    TRANSMISSION = "Tf "
    SPECULAR_EXPONENT = "Ns "


    def __init__(self, name = "default_blue"):
        """

        """
        self.name :str = name 
        self.ka : List(int)= [0.0,0.0,0.0] #ambient color. R G B
        self.kd : List(int) = [0.0,0.0,255]  #diffuse color. R G B We default to blue
        self.ks : List(int) = [255,255,255] #spec color
        self.tr : float = 0.0 #transparency: sometime d (dissolve) = 1.0 - Tr
        self.tf : List(int) = [0,0,0] #transmission R G B
        self.Ns : float = 0.0 #specular exponent...the focus of specular highlight. typ 0 to 1000 

    def __str__(self):
        return " Basic material: %s ka: %s kd : %s  ks %s" % (self.name, self.ka,self.kd,self.ks)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def read_mtlfile(full_mtl_filepath : str):


        def rgb(line : str):
            """
            converts obj-format indexed color string to rgb integer array
            eg 0 0.5 1.0 -> [0 128 255]
            """
            return [int(i* 255) for i in map(float, line.strip().split())]

        current_mtl = None        
        my_mtls = {} 

        with open(full_mtl_filepath) as fp:
            for i, line in enumerate(fp):
                if line.startswith(_BasicWavMaterial.NEW_MATERIAL):
                    if current_mtl is not None:
                        my_mtls[current_mtl.name] = current_mtl
                    # start new material
                    name = line[len(_BasicWavMaterial.NEW_MATERIAL):].strip()
                    current_mtl = _BasicWavMaterial(name)
                elif line.startswith(_BasicWavMaterial.AMBIENT_COLOR):
                    line = line[len(_BasicWavMaterial.AMBIENT_COLOR):] # remove ka and whitespace
                    current_mtl.ka = rgb(line)
                elif line.startswith(_BasicWavMaterial.DIFFUSE_COLOR):
                    line = line[len(_BasicWavMaterial.DIFFUSE_COLOR):] # remove kd and whitespace
                    current_mtl.kd = rgb(line)
                elif line.startswith(_BasicWavMaterial.SPECULAR_COLOR):
                    line = line[len(_BasicWavMaterial.SPECULAR_COLOR):] # remove ks and whitespace
                    current_mtl.ks = rgb(line)
                elif line.startswith(_BasicWavMaterial.TRANSPARENCY):
                    line = line[len(_BasicWavMaterial.TRANSPARENCY):].strip() # remove tr and whitespace
                    current_mtl.tr = float(line)
                elif line.startswith(_BasicWavMaterial.DISSOLVE):
                    line = line[len(_BasicWavMaterial.DISSOLVE):].strip() # remove d and whitespace
                    current_mtl.tr = 1.0 - float(line)
                elif line.startswith(_BasicWavMaterial.TRANSMISSION):
                    line = line[len(_BasicWavMaterial.TRANSMISSION):] # remove tf and whitespace
                    current_mtl.tr = rgb(line)
        
        #pick up the last one.                       
        if current_mtl is not None:
            my_mtls[current_mtl.name] = current_mtl

        return my_mtls
