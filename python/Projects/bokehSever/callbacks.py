from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show
import pandas as pd
output_file("js_on_change.html")

x = [x*0.005 for x in range(0, 200)]
y = x

x = pd.to_datetime(['2018-06-1 18:30:00', '2018-06-12 19:30:00','2018-06-12 20:30:00'	 ])
y = [2,56,4]

source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400, x_axis_type="datetime")
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        x[i] = x[i] + f
        y[i] = y[i]
    }
    source.change.emit();
""")

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
slider.js_on_change('value', callback)

layout = column(slider, plot)

show(layout)