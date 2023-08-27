import io
from base64 import b64encode

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import scripts.simulation as sim
from scripts.animation import *
from scripts.utils import Unif

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder="assets")
server = app.server

fig = draw_figure(5, [], [], add_frames=False)


# define app layout using dash html and dcc components
app.layout = html.Div(id="page", children=[
        html.Div(
            id='left_col',
            children=[
                        html.Div(
                            id='graph_parent',
                            children=[dcc.Graph(figure=fig, id='live-graph', animate=True)]
                                ),
                        dcc.Interval(id='graph-update', interval=1 * 1000),
                    ]
                ),
        html.Div(
            id="right_col",
            children=[
                html.Div(id="params", children=[
                        html.Label("Set your parameters", id="label"),
                        html.Label('Width of the road', id="d_label"),
                        dcc.Input(
                            id="d", type="number", value=10,
                            min=5, max=15,
                                ),
                        html.Label('Drinker velocity', id="v_d_label"),
                        dcc.Input(
                            id="v_d", type="number", value=1
                        ),
                        html.Label("Minimal cars' velocity", id='v_m_label'),
                        dcc.Input(
                            id="v_m", type="number", value=10
                                ),
                        html.Label("Maximal cars' velocity", id='v_M_label'),
                        dcc.Input(
                            id="v_M", type="number", value=20
                                ),
                        html.Label("Traffic congestion", id="traffic_label"),
                        dcc.Slider(
                            id="slider",
                            min=0,
                            max=1,
                            step=0.1,
                            marks={
                                "0": '0',
                                "0.2": '0.2',
                                "0.4": '0.4',
                                "0.6": '0.6',
                                "0.8": "0.8",
                                "1": '1'
                            },
                            value=0.5,
                        ),
                        html.Div(
                            [html.Button('Setup', id='simulate', n_clicks=0)]
                        ),
                        html.A(
                            html.Button("Download HTML", id="download_button"),
                            id="download",
                            href="data:text/html;base64,",
                            download="animation.html"
                        )
                        ]),
                     ]
                )
        ]
)


@app.callback(Output('graph_parent', 'children'),
              Input('simulate', 'n_clicks'),
              Input('d', 'value'),
              Input('v_d', 'value'),
              Input('v_m', 'value'),
              Input('v_M', 'value'),
              Input('slider', 'value')
              )
def simulate(n, d, v_d, v_m, v_M, freq):
    """
    Return a dcc.Graph with animation.
    :param n: number of button clicks
    :param d: road width
    :param v_d: drinker's velocity
    :param v_m: cars' minimal velocity
    :param v_M: cars' maximal velocity
    :param freq: cars' arrivals frequency
     """
    drinker, cars = sim.simulate(d, v_d, Unif(freq, freq+0.1), Unif(freq, freq+0.1), v_m, v_M)
    new_fig = draw_figure(d, drinker, cars, True)
    return dcc.Graph(figure=new_fig, id=f'live-graph_{n}', animate=True)


@app.callback(Output('download', 'href'),
              Input('graph_parent', 'children'),
              Input('download', 'n_clicks')
              )
def load_graph(graph, n):
    """Return a html file with the animation."""
    fig_ = go.Figure(graph['props']['figure'])
    buffer = io.StringIO()
    fig_.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()
    return "data:text/html;base64," + encoded


if __name__ == '__main__':
    app.run_server(debug=True)
