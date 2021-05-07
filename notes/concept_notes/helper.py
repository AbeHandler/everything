import numpy as np
import altair as alt
import functools


def make_altair_object_labels(X, Y, L):
    bi = []
    for x, y, l in zip(X, Y, L):
        bi.append({"x": x, "y": y, "label": l})
    return alt.Data({"values": bi})


def make_altair_object(X, Y):
    bi = []
    for x, y in zip(X, Y):
        bi.append({"x": x, "y": y})
    return alt.Data({"values" : bi})


def make_bar_chart(size, opacity, X, Y, L = None):
    data = make_altair_object(X, Y)
    if L is not None:
        data = make_altair_object_labels(X, Y, L)
    return alt.Chart(data).mark_bar(size=10, opacity=.2).encode(
        x='x:Q',  # specify ordinal data
        y='y:Q',  # specify quantitative data
    )
    return


def make_guide_lines(s):
    guide_lines = []

    for x, x_2 in zip(s, [i ** 2 for i in s]):
        Xs = [x, x]
        Ys = [0, x_2]
        dt = make_altair_object(X=Xs, Y=Ys)
        guide_lines.append(alt.Chart(dt).mark_line(opacity=.1, color="black").encode(
            x='x:Q',  # specify ordinal data
            y='y:Q',  # specify quantitative data
        ))
    return guide_lines


def make_scatter_chart(X, Y,
                       opacity=.2,
                       size=100,
                       color="darkblue",
                       domain=None):
    data = make_altair_object(X, Y)

    if domain is None:
        altx = 'x:Q'
    else:
        min_, max_ = domain
        altx = alt.X('x:Q', scale=alt.Scale(domain=(min_, max_)))

    alty = 'y:Q'

    return alt.Chart(data).mark_point(size=size,
                                      opacity=opacity,
                                      color=color,
                                      filled=True,
                                      clip=True).encode(
        x=altx,  # specify ordinal data
        y=alty,  # specify quantitative data
    )


def make_scatter_chart_with_labels(X, Y, L,
                                   color="blue",
                                   size=200,
                                   opacity=.1,
                                   domain=None):

    dt = make_altair_object_labels(X, Y, L)

    if domain is None:
        altx = 'x:Q'
    else:
        min_, max_ = domain
        altx = alt.X('x:Q', scale=alt.Scale(domain=(min_, max_)))

    alty = 'y:Q'

    expected_x = alt.Chart(dt).mark_point(opacity=opacity,
                                          size=size,
                                          color=color,
                                          clip=True,
                                          filled=True).encode(
        x=altx,  # specify ordinal data
        y=alty,  # specify quantitative data
    )

    labels = expected_x.mark_text(
        align='left',
        baseline='bottom',
        yOffset=-4,
        xOffset=-2,
        fill="white",
        opacity=1,
        fillOpacity=1,
        dx=16,
        stroke="black"
    ).encode(
        text='label:N'
    )

    return expected_x, labels


point_size = 50
expectation_size = 200
point_opacity = .2
expectation_opacity = .9
line_opacity=.2