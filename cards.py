import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq

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

def wheel_slider_card():
    """
    :return: A Div containing controls for Pyrograph.
    """
    return html.Div(
        id="wheel-knob-card",
        children=[
            html.H5('Wheel Size'),
            daq.Slider(
                value=.66,
                color='#4A9DFF',
                id='size-input',
                max=0.95,
                min=0.05,
                step=0.01,
                className='slider columns',
            ),
            
            html.H5('Hole Position'),
             daq.Slider(
                value=.66,
                color='#FF4A4C',
                id='hole-input',
                max=0.95,
                min=0.05,
                step=0.01,
                className='slider columns',
            ),
            html.H5('Start Angle'),
             daq.Slider(
                value=0,
                color='#C068FA',
                id='start-ang',
                max=90,
                min=0,
                step=0.5,
                className='slider columns',
            ),
        ],
    )

def render_slider_card():
    """
    :return: A Div containing controls for Pyrograph.
    """
    return html.Div(
        id="render-knob-card",
        children=[
            html.H5('Line Width'),
             daq.Slider(
                value=2.5,
                color='#02A90E',
                id='line-width',
                max=10,
                min=1,
                step=0.5,
                className='slider columns',
            ),
            html.H5('Revolutions'),
             daq.Slider(
                value=1,
                color='#F7B801',
                id='revs',
                max=10,
                min=1,
                step=1,
                className='slider columns',
            ),
        ],
    )

def wheel_led_card():
    return html.Div(
        id='wheel-led-card',
        children=[
            daq.LEDDisplay(
                id="size-display",
                color='#4A9DFF',
                size=25,
                value=0.66,
                className="threep columns",
            ),
            daq.LEDDisplay(
                id="hole-display",
                color='#FF4A4C',
                size=25,
                value=0.66,
                className="threep columns",
            ),
            daq.LEDDisplay(
                id="angle-display",
                color='#C068FA',
                size=25,
                value=0.0,
                className="threep columns",
            ),
        ],
        className='led-displays',
    )

def render_led_card():
    return html.Div(
        id='render-led-card',
        children=[
            daq.LEDDisplay(
                id="width-display",
                color='#02A90E',
                size=25,
                value=0.66,
                className="threet columns",
            ),
            daq.LEDDisplay(
                id="revs-display",
                color='#F7B801',
                size=25,
                value=1,
                className="threet columns",
            ),
        ],
        className='led-displays',
    )

def spin_buttons():
    return html.Div(
        children=[
            html.Button(
                'Spin!',
                id='sp_butt',
                n_clicks=0,
                className='buttons',
            ),
            html.Button(
                'Undo!',
                id='un_butt',
            n_clicks=0,
            className='buttons',
            ),
        ]
    )

