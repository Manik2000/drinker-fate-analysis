import plotly.graph_objects as go


def draw_figure(d, drinker, cars, add_frames=False):
    """
    Return a plotly figure with containing an animation.
    :param d: width of the road
    :param drinker: drinker positions
    :param cars: cars' positions
    :param add_frames: boolean value deciding if to add frames to an animation
    """
    fig = go.Figure()
    fig.update_xaxes(range=[0, 1000])
    fig.update_yaxes(range=[0, 50])
    # create a road
    fig.add_shape(
            type="rect",
            x0=0, y0=25-d, x1=1000, y1=25+d,
            fillcolor='black',
            layer="below"
        )
    fig.add_shape(
            type="rect",
            x0=0, y0=25+d, x1=1000, y1=50,
            fillcolor='#696969',
            layer="below"
        )
    fig.add_shape(
            type="rect",
            x0=0, y0=0, x1=1000, y1=25-d,
            fillcolor='#696969',
            layer="below"
        )
    fig.add_shape(
            type="line",
            x0=0, y0=25, x1=1000, y1=25,
            line=dict(
                color="white",
                width=3,
                dash="dash"
            )
        )
    fig.update_shapes(layer="below")
    fig.add_trace(go.Scatter())
    fig.add_trace(go.Scatter())
    fig.update_xaxes(fixedrange=True, showgrid=False)
    fig.update_yaxes(fixedrange=True, showgrid=False)
    # animation setup
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        updatemenus=[
            dict(
                type="buttons",
                buttons=[dict(
                    label=15 * " " + "Play" + 15 * " ",
                    method="animate",
                    args=[
                        None,
                        {"frame": {"duration": 120, "redraw": False},
                         "fromcurrent": True,
                         "transition": {"duration": 1}}
                    ]
                ),
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                          "mode": "immediate",
                                          "transition": {"duration": 0}}],
                        "label": 15 * " " + "Pause" + 15 * " ",
                        "method": "animate"
                    },
                ],

                showactive=True,
                direction='left',
                x=0.1,
                xanchor="left",
                y=-0.2,
                yanchor="bottom",
                font={'size': 20}
            ),

        ],
        title={
            'text': "Drinker fate simulation",
            'y': 0.95,
            'x': 0.5,
            'font': {'size': 40},
            'xanchor': 'center',
            'yanchor': 'top'}

    )
    # adding frames
    if add_frames:
        fig.frames = [go.Frame(
            data=[
                go.Scatter(
                    x=[k[0]-k[2]*26 for k in y],
                    y=[k[1] for k in y],
                    mode="markers",
                    marker=dict(color="blue",
                                size=42, symbol="square")
                ),
                go.Scatter(
                    x=[x[0]],
                    y=[x[1]],
                    mode="markers",
                    marker=dict(color="red", size=10))
            ]) for x, y in zip(drinker, cars)]
    return fig
