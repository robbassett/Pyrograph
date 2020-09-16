import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq

import plotly.graph_objects as go
import numpy as np

def one_orbit(wheel_size,hole_pos,N):

    r = wheel_size
    rho = wheel_size*hole_pos

    dm = divmod(1.,(1.-r))
    orb = 2.*np.pi*(dm[0]-1)
    if orb == 0:
        orb = 2.*np.pi

    theta = np.linspace(float(N)*orb,float(N+1)*orb,1000)
    cx = (1.-r)*np.cos(theta)
    cy = (1.-r)*np.sin(theta)
    itheta = ((-1.)*(1.-r)/r)*theta
    ix = rho*np.cos(itheta)
    iy = rho*np.sin(itheta)

    return cx+ix,cy+iy

app = dash.Dash(__name__)
#server = app.server

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="title-card",
        children=[
            html.H4("Pyrograph (beta)"),
        ]
    )

def generate_about():
    return html.Div(
        id='about-card',
        children=[
            html.H2('About Pyrograph'
            ),
            html.P('Did you have a Spirograph as a kid? Did you always skip the teeth and ruin your Spirograph artwork? Did this make you throw your Spirograph through a window? Rage no more! This app never skips or wastes paper, f&*! you Spirograph!'
            ),
        ],
    )

def slider_card():
    """
    :return: A Div containing controls for Pyrograph.
    """
    return html.Div(
        id="knob-card",
        children=[
            html.H5('Wheel Size'),
            daq.Slider(
                value=.66,
                color='#4A9DFF',
                id='size-input',
                max=0.95,
                min=0.05,
                step=0.01,
                className='twelve columns',
            ),
            html.H5('Hole Position'),
             daq.Slider(
                value=.66,
                color='#FF4A4C',
                id='hole-input',
                max=0.95,
                min=0.05,
                step=0.01,
                className='twelve columns',
            ),
            html.H5('Line Width'),
             daq.Slider(
                value=1,
                color='#02A90E',
                id='line-width',
                max=10,
                min=1,
                step=0.5,
                className='twelve columns',
            ),
        ],
    )

def led_card():
    return html.Div(
        id='led-card',
        children=[
            daq.LEDDisplay(
                id="size-display",
                color='#4A9DFF',
                size=32,
                value=0.66,
                className="four columns",
            ),
            daq.LEDDisplay(
                id="hole-display",
                color='#FF4A4C',
                size=32,
                value=0.66,
                className="four columns",
            ),
            daq.LEDDisplay(
                id="width-display",
                color='#02A90E',
                size=32,
                value=0.66,
                className="four columns",
            ),
        ],
        className='led-displays',
    )

app.layout = html.Div(
    id="app-container",
    children=[
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                dcc.Tabs([
                    dcc.Tab(label='About', children=[
                        html.Div(
                            id='about-column',
                            children=[generate_about()]
                        ),
                    ]),
                    dcc.Tab(label='Wheel Control', children=[
                        html.Div(
                            id='control-column',
                            children=[description_card(), slider_card(), led_card()]
                        ),
                        html.Div(
                            children=[
                                html.Button(
                                    'Spin!',
                                    id='sp_butt',
                                    n_clicks=0,
                                    className='five columns',
                                    style={'marginTop':'1.5em'}
                                ),
                                html.Button(
                                    'Undo!',
                                    id='un_butt',
                                    n_clicks=0,
                                    className='five columns',
                                    style={'marginTop':'1.5em'}
                                ),
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            className="left-panel-color-picker",
                            children=[
                                html.Hr(),
                                daq.ColorPicker(
                                    id="color-picker",
                                    label=" ",
                                    value=dict(rgb=dict(r=1,g=105,b=200,a=1)),
                                    size=370,
                                    className='eleven columns',
                                ),
                            ]
                        ),
                    ]),
                ]),
            ],
        ),
        # Right Column
        html.Div(
            id='right-column',
            className='eight columns',
            children=[
                html.Div(
                    id='pyrograph-card',
                    children=[
                        dcc.Graph(id='pyrograph'),
                    ],
                ),
            ],
        ),
    ]
)

# Callbacks for knob inputs
@app.callback(
    [
        Output("size-display", "value"),
        Output("hole-display", "value"),
        Output('sp_butt','n_clicks'),
    ],
    [
        Input("size-input", "value"),
        Input("hole-input", "value"),
    ]
)
def update_size_display(v1,v2):
    return v1,v2,0

@app.callback(
    Output('width-display','value'),
    Input('line-width','value')
)
def update_lw_display(v1):
    return v1

@app.callback(
    Output('pyrograph','figure'),
    [
        Input('sp_butt','n_clicks'),
        Input('un_butt','n_clicks'),
    ],
    state=[
        State('pyrograph','figure'),
        State('size-input','value'),
        State('hole-input','value'),
        State('line-width','value'),
        State('color-picker','value'),
    ]
)
def update_pyrograph(btn,ubt,fig,sz,ho,wi,cl):
    
    if btn == 0:
        fig = go.Figure(fig)
        fig.update_xaxes(range=[-1.,1.])
        fig.update_yaxes(range=[-1.,1.])
        fig.update_layout(
            yaxis=dict(
                scaleanchor='x',
                scaleratio=1,
                showticklabels=False
            ),
            xaxis=dict(showticklabels=False),
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            autosize=False,
            width=800,
            height=800
        )

    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'un_butt':
            fig['data'].pop()
            fig = go.Figure(fig)
            
        else:
            if btn != 0:
                fig = go.Figure(fig)
                col = cl['rgb']
                t = [col['r'],col['g'],col['b'],col['a']]
                rgba = f'rgba({t[0]},{t[1]},{t[2]},{t[3]})'
                x,y = one_orbit(sz,ho,btn-ubt)
                fig.add_trace(go.Scatter(x=x,y=y,mode='lines',line=dict(color=rgba,width=wi)))
    
    return fig
        

if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=True)
    #app.run_server()
