import cairo

class Generate_Chart:

    # note : if you are using pycha.bar.HorizontalBarChart
    # x-y axis is not the normal type in chinese understanding...
    # here x = ver, and y = hor

    '''
    for color, see below choice
    basicColors = dict(
        red='#6d1d1d',
        green=DEFAULT_COLOR,
        blue='#224565',
        grey='#444444',
        black='#000000',
        darkcyan='#305755',
        )
    '''

    def barChart(self, input, output, title, x_name, y_name, chartFactory, charColor):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 1024)

        dataSet = (
            (x_name, [(i, l[1]) for i, l in enumerate(input)]),
            )

        options = {
            'axis': {
                'x': {
                    'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(input)],
                    'label': y_name,
                    'rotate': 25
                },
                'y': {
                    'tickCount': 5,
                    'rotate': 25,
                    'labelWidth':80,
                    'label': x_name
                }
            },
            'yvals': {
                'show': True
            },
            'background': {
                'chartColor': '#ffeeff',
                'baseColor': '#ffffff',
                'lineColor': '#444444'
            },
            'colorScheme': {
                'name': 'gradient',
                'args': {
                    'initialColor': charColor
                },
            },
            'legend': {
                'hide': True,
            },
            'padding': {
                'left': 20,
                'right': 60,
                'top': 20,
                'bottom': 20
            },
            'title': title
        }
        chart = chartFactory(surface, options)

        chart.addDataset(dataSet)
        chart.render()

        surface.write_to_png(output)

