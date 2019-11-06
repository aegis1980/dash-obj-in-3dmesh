Import a Wavefront OBJ file into a plot.ly Dash 3dMesh

```
pip install git+https://github.com/aegis1980/dash-obj-in-3dmesh.git
```


### Some notes:
 
#### File locations
Put your wavefront obj & mtl file in 'data/obj' directory (this is the default). Alternatively pass a path to:
```python
import_geometry(obj_names : List[str], path = _config.GEOMETRY_DIR)
```
#### Geometry
* Only triangulated meshes supported (i.e 3 vertices per face). Sort this out in your modelling software (e.g. Rhino)
* Textures, normals, groups are all ignored - only vertices, faces, materials and object names are parsed and passed to Dash graph as mesh data.
#### Materials
Only basic materials supported in mtl file:
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
Only the value for `Kd` is used - so set this as your colour (in modelling software)

### Code example

```python
import dash
from dash_obj_in_3dmesh import geometry_tools, wav_obj


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

layout = return html.Div([dcc.Graph(
                        id="graph",
                        figure={
                            "data": geometry_tools.import_geometry([model_name]),
                            "layout": plot_layout,
                        },
                        config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
                    )])
```

