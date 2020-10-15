import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq

import plotly.graph_objects as go
import numpy as np
from cards import *
from wheel_drawer import draw_wheel

def one_orbit(wheel_size,hole_pos,N,theta_start=0.,revs=1.):

    rang = theta_start*np.pi/180.
    r = wheel_size
    rho = wheel_size*hole_pos

    orb = 2.*np.pi*(r)

    theta = np.linspace(float(N*revs)*orb,float(N+1)*revs*orb,1000)
    cx = (1.-r)*np.cos(theta+np.pi)
    cy = (1.-r)*np.sin(theta+np.pi)
    itheta = ((-1.)*(1.-r)/r)*theta
    ix = rho*np.cos(itheta)
    iy = rho*np.sin(itheta)

    rmat = np.array([
            [np.cos(rang),(-1.)*np.sin(rang)],
            [np.sin(rang),np.cos(rang)]
        ])

    vs = np.vstack((cx+ix,cy+iy))
    vs = np.dot(vs.T,rmat).T

    return vs[0],vs[1]

app = dash.Dash(__name__)
server = app.server

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.Img(id="logo", src=app.get_asset_url("pyrograph_logo.png")),
                ],
            ),
        ]
    )

def about_card():
    return html.Div(
        id='about-card',
        children=[
            html.H2(
                'About Pyrograph',
                className='about columns'
            ),
            html.P('Did you have a Spirograph as a kid? Did you always skip the teeth and ruin your Spirograph artwork? Did this make you throw your Spirograph through a window? Rage no more! This app never skips or wastes paper, screw you Spirograph!',
                    className='descript columns',
            ),
            html.Div(
                html.Img(src=app.get_asset_url('spiro.jpg'),
                className='descript columns',
                )
            ),
        ],
    )

app.layout = html.Div(
    id="app-container",
    children=[
        build_banner(),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                dcc.Tabs([
                    dcc.Tab(label='About', children=[
                        html.Div(
                            id='about-column',
                            children=[about_card()]
                        ),
                    ]),
                    dcc.Tab(label='Wheel', children=[
                        html.Div(
                            id='wheel-control-column',
                            children=[wheel_slider_card(), wheel_led_card()]
                        ),
                        html.Div(
                            id='wheelie',
                            children=[
                                html.Div(
                                    id='wheel-card',
                                    children=[
                                        dcc.Graph(
                                            id='wheel-image',
                                            className='wheelim columns',
                                            ),
                                    ],
                                ),
                            ],
                        ),
                    ]),
                    dcc.Tab(label='Render', children=[
                        html.Div(
                            id='render-control-column',
                            children=[render_slider_card(), render_led_card()]
                        ),
                        html.Div(
                            className="left-panel-color-picker",
                            children=[
                                html.Hr(),
                                daq.ColorPicker(
                                    id="color-picker",
                                    label=" ",
                                    value=dict(rgb=dict(r=1,g=105,b=200,a=1)),
                                    size=370,
                                    className='colorpicker columns',
                                ),
                            ]
                        ),
                    ]),
                ]),
                html.Div(
                    children=[spin_buttons()],
                ),
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
        Output('angle-display', 'value'),
        Output('sp_butt','n_clicks'),
    ],
    [
        Input("size-input", "value"),
        Input("hole-input", "value"),
        Input('start-ang', 'value'),
    ]
)
def update_size_display(v1,v2,v3):
    return v1,v2,v3,0

@app.callback(
    Output('width-display','value'),
    [Input('line-width','value')]
)
def update_lw_display(v1):
    return v1

@app.callback(
    Output('revs-display','value'),
    [Input('revs','value')]
)
def update_rev_display(v1):
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
        State('start-ang','value'),
        State('revs','value'),
    ]
)
def update_pyrograph(btn,ubt,fig,sz,ho,wi,cl,sta,revs):
    
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
                x,y = one_orbit(sz,ho,btn-ubt,theta_start=sta,revs=revs)
                fig.add_trace(go.Scatter(x=x,y=y,mode='lines',line=dict(color=rgba,width=wi)))
    
    return fig

@app.callback(
    Output('wheel-image','figure'),
    [
        Input('size-input','value'),
        Input('hole-input','value'),
    ],
)
def update_wheel_im(whs,hos):
    fig = go.Figure()
    fig.update_xaxes(range=[-1.2,1.2])
    fig.update_yaxes(range=[-1.2,1.2])

    shps = draw_wheel(whs,hos)
    fig.update_layout(
        shapes=shps,
        yaxis=dict(
                scaleanchor='x',
                scaleratio=1,
                showticklabels=False
        ),
        xaxis=dict(showticklabels=False),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=300,
        height=300,
        margin=go.layout.Margin(
            l=70,
            r=0,
            b=0,
            t=0
        )
    )
    return fig

if __name__ == '__main__':
    #app.run_server(host='127.0.0.1',debug=True)
    app.run_server()
