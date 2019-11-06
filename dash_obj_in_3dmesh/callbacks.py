# built-in py modules
import json

# 3rd party modules
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Local modules
from app import app

@app.callback(Output('graph', 'figure'),
              [Input('fresnel_slider','value')])
def change_lighting(fresnel):
    return fresnel

#@app.callback(Output('hover-data', 'children'),
#              [Input('graph', 'hoverData')])

#def display_hover_data(hover_data):
#    return json.dumps(hover_data, indent=2)

#@app.callback(Output('hover-data', 'children'),
#              [Input('graph', 'figure')],
#                [State('graph', 'figure')])

#def display_hover_data(figure, statefig):
#    return json.dumps(statefig['layout']['scene'], indent=2)
