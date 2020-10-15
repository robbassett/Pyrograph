import plotly.graph_objects as go
import numpy as np

def draw_wheel(wheel_size,hole_position):
    outer_circ = dict(
        type='circle',
        xref='x',
        yref='y',
        x0=-1,
        y0=-1,
        x1=1,
        y1=1,
        line_color='black',
    )

    inner_circ = dict(
        type='circle',
        xref='x',
        yref='y',
        x0=-1,
        y0=(-1.)*wheel_size,
        x1=-1.+(2.*wheel_size),
        y1=wheel_size,
        line_color='red',
        fillcolor='lightcoral',
    )

    whc = -1+wheel_size
    hrd = wheel_size*hole_position
    hole_circ = dict(
        type='circle',
        xref='x',
        yref='y',
        x0=whc-hrd-.02,
        y0=-0.02,
        x1=whc-hrd+.02,
        y1=.02,
        fillcolor='black'
    )

    return [outer_circ,inner_circ,hole_circ]
    
