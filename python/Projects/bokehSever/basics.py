import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.stocks import AAPL
from bokeh.models import DatetimeTickFormatter
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column

df = pd.DataFrame(AAPL)
df['date'] = pd.to_datetime(df['date'])

df_date = ['2018-06-1 18:30:00', '2018-06-12 19:30:00','2018-06-12 20:30:00'	 ]
df_data = [2,56,4]

source = ColumnDataSource(data=dict(x=df_date, y=df_data))

output_file("datetime.html")

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = y[i] + f
    }
    source.change.emit();
""")



# create a new plot with a datetime axis type
p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")



p.line(pd.to_datetime(df_date), df_data, color='navy', alpha=0.5)

slider = Slider(start=1, end=1000, value=1, step=1, title="power")
slider.js_on_change('value', callback)

layout = column(slider, p)
try:
    show(layout)
except:
    output_file("datetime.html")
    show(p)