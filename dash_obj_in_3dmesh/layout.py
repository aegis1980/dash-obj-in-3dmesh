#built-in py modules
import os

#3rd party modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_colorscales as dcs
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


# local modules
import geometry_tools

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


control_panel = [
    html.Pre(
        id = 'hover-data',
    ),
    dcc.Slider(
        id = 'fresnel_slider',
        min=0,
        max=10,
        step=0.5,
        value=1
    )  
]

# control box type overlay, on left of screen
overlay = dbc.Container(
            dbc.Row([
                dbc.Col(
                    children = dbc.FormGroup(control_panel)
                , width=2),
            ],justify='start'
        ),id = 'overlay', fluid = True
    )


def make_layout():
    """

    """
    return html.Div([dcc.Graph(
                        id="graph",
                        figure={
                            "data": geometry_tools.import_geometry(["test"]),
                            "layout": plot_layout,
                        },
                        config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
                    ),
                     overlay
                     ])

