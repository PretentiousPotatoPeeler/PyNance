import pygal


def line_chart(values, name, height=200):
    dateline = pygal.DateLine(x_label_rotation=25, height=height)
    dateline.add(name, values)
    return dateline.render_response()
