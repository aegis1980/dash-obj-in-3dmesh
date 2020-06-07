# Wavefront OBJ importer for the plotly Dash framework

#### *Dash is a Python framework for building analytical web applications. This library helps you to get 3D ObJ into the framework's 3dmesh graph type*

Source is here:
```
https://github.com/aegis1980/dash-obj-in-3dmesh.git
```
Also on pypi, installed using:
```
pip install dash-obj-in-3dmesh
```
---
### Some notes:
 
#### File locations
Put your wavefront obj & mtl file in 'data/obj' directory in the root directory of your Dash app. Alternatively pass a path to:
```python
import_geometry(obj_names : List[str], path = _config.GEOMETRY_DIR)
```
#### Geometry
* **v4.0** Added support importing OBJ files with quads. Dash graph.Mesh3d can only display triangulated meshes. Imported quad are split in `mesh_tools.split_quad()` into two tris with the fold line on the quad diagonal which produces the least curvature (i.e. the widest angle between the tri normals)
* Textures, normals and everything else are ignored - only vertices, faces, materials, groups and object names are parsed and passed to Dash graph as mesh data. 
* ...so to speeden things up strip all that data out of your files pre-deployment 
#### Materials
obj file can have an accompanying materials file, but only basic materials supported in mtl file:
e.g:
```
newmtl diffuse_Green
Ka 0.0000 0.0000 0.0000
Kd 0.0000 1.0000 0.0000
Ks 1.0000 1.0000 1.0000
Tf 0.0000 0.0000 0.0000
d 1.0000
Ns 0.0000
```
Only the value for `Kd` is used - so set this as your colour (in modelling software).

### Code example

```python
import dash
import dash_obj_in_3dmesh


model_name = "test" #.obj & .mtl files in data/obj

axis_template = {
    "showbackground": False,
    "visible" : False
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    'uirevision':'same_all_the_time', #this keeps camera position etc the same when data changes.
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectmode" : "data",
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

def layout():
 return html.Div([dcc.Graph(
          id="graph",
          figure={
              "data": geometry_tools.import_geometry([model_name]),
              "layout": plot_layout,
          },
          config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
      )])
      
app = Dash()
app.layout = layout

app.run_server()
```



