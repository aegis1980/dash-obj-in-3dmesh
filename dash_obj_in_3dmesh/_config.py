import pathlib

DATA_PATH = pathlib.Path.cwd().joinpath('data').resolve()
GEOMETRY_DIR = 'obj' #(in DATA_PATH)
RESULTS_DIR = 'results' #(in DATA_PATH)

# found this somewhere, thought it might me useful.
COLOR_SCALES  = ['Blackbody',
'Bluered',
'Blues',
'Earth',
'Electric',
'Greens',
'Greys',
'Hot',
'Jet',
'Picnic',
'Portland',
'Rainbow',
'RdBu',
'Reds',
'Viridis',
'YlGnBu',
'YlOrRd']

SCHEME_PARAMETER = 'scheme'

SCENARIO_PARAMETERS = [SCHEME_PARAMETER, 'roof_area', 'roof_vlt' ,'fac_vlt', 'can_vlt']

SCHEMES = {
    'tri' : 'Triangular',
    'current' : 'PD radial strips',
    'strip' : 'Circumferential strips'
    }
