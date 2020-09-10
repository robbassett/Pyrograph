from Pyrograph import *

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq

import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server
pyro = 0

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="title-card",
        children=[
            html.H3("Pyrograph (beta)"),
            html.Div(
                id="intro",
                children="Create virtual spyrograph art.",
            ),
        ],
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

def knob_card():
    """
    :return: A Div containing controls for Pyrograph.
    """
    return html.Div(
        id="knob-card",
        children=[
            daq.Knob(
                value=0.66,
                label='Wheel Size',
                id='size-input',
                labelPosition='bottom',
                size=95,
                max=0.95,
                min=0.05,
                className='five columns',
            ),
             daq.Knob(
                value=0.66,
                label='Hole Position',
                id='hole-input',
                labelPosition='bottom',
                size=95,
                max=0.95,
                min=0.05,
                className='five columns',
            ),
        ],
    )

def led_card():
    return html.Div(
        id='led-card',
        children=[
            daq.LEDDisplay(
                id="size-display",
                size=32,
                value=0.666,
                className="six columns",
            ),
            daq.LEDDisplay(
                id="hole-display",
                size=32,
                value=0.666,
                className="six columns",
            ),
        ],
        className='led-displays',
    )

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=["/assets/dash-logo-new.png"],
        ),
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
                            children=[description_card(), knob_card(), led_card()]
                        ),
                        html.Br(),
                        html.Hr(),
                        html.Div(
                            html.Button(
                                'Spin!',
                                id='sp_butt',
                                n_clicks=0,
                                className='twelve columns'
                            ),
                        ),
                        html.Br(),
                        html.Div(
                            className="left-panel-color-picker",
                            children=[
                                html.Hr(),
                                daq.ColorPicker(
                                    id="color-picker",
                                    label=" ",
                                    value=dict(hex="#0054A6"),
                                    size=300,
                                    className='twelve columns',
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
        Output('sp_butt','n_clicks')
    ],
    [
        Input("size-input", "value"),
        Input("hole-input", "value")
    ]
)
def update_size_display(v1,v2):
    return v1,v2,0

@app.callback(
    Output('pyrograph','figure'),
    [Input('sp_butt','n_clicks'),],
    state=[
        State('pyrograph','figure'),
        State('size-input','value'),
        State('hole-input','value'),
        State('color-picker','value'),
    ]
)
def update_pyrograph(btn,fig,sz,ho,cl):
    global pyro
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
    
    elif btn == 1:
        fig = go.Figure(fig)
        pyro = Pyrograph(hole=ho,inner_frac=sz)
        for i in range(2): pyro.one_orbit()

        fig.add_trace(go.Scatter(x=pyro.x[-1],y=pyro.y[-1],mode='lines',line=dict(color=cl['hex'])))
        
        
        
    else:
        fig = go.Figure(fig)
        pyro.one_orbit()
        fig.add_trace(go.Scatter(x=pyro.x[-1],y=pyro.y[-1],mode='lines',line=dict(color=cl['hex'])))

    return fig

if __name__ == '__main__':
    #app.run_server(host='127.0.0.1',debug=True)
    app.run_server()
