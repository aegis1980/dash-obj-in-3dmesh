

# builtin modules
import pathlib
from typing import List

#3rd party modules
import numpy as np
import plotly.graph_objs as go

#Local modules
import _config 
import wav_obj

def make_ployly_mesh3d(
    vertices,
    faces,
    name = '',
    color='grey',
    colorscale = None,
    opacity = 1,
    flatshading=False,
    intensities = None,
    facecolors = None,
    showscale=False,
    hoverinfo='none',
    hovertemplate = '',
    customdata = None,
    vertexcolor = []
):

    x, y, z = vertices.T
    I, J, K = faces.T
  

    trace = go.Mesh3d(
        x=x,
        y=y,
        z=z,
        colorscale = colorscale,
        color = color,
        intensity = intensities,
        facecolor= facecolors,
        opacity = opacity,
        flatshading = flatshading,
        hoverinfo=hoverinfo,
        hovertemplate = hovertemplate,
        vertexcolor = vertexcolor,
        i = I,
        j = J,
        k = K,
        customdata = None,
        name = name,
        showscale = showscale,
        lighting = {
            "ambient": 0.0,
            "diffuse": 0.8,
            "fresnel": 1,
            "specular": 1.5,
            "roughness": 1,
        },
        lightposition = {"x": 1000, "y": 2000, "z": 1000},   
        )

    return trace




def import_geometry(obj_names : List[str], path = _config.GEOMETRY_DIR):
    c = []
    for component in obj_names:
        traces = create_mesh_data(component,path)
        c.extend(traces)
    return c


def create_mesh_data(component : str, path = _config.GEOMETRY_DIR):
    """
    Create mesh-for-plotly from single obj file
    """

    data = []
    wav_objs = wav_obj.WavObject.read_objfile(component, path, split = False)

    for i, obj in enumerate(wav_objs):
        mesh = make_ployly_mesh3d(
            obj.vertices,
            obj.faces,
            name = obj.name,
            facecolors = obj.face_colors,
            opacity = obj.opacities[0],
            vertexcolor = obj.vertice_colors,
        )
        data.append(mesh)

    return data



