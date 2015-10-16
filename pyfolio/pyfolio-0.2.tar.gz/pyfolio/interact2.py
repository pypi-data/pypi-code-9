from __future__ import print_function
from copy import copy
from collections import OrderedDict
import numpy as np

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl

import pyfolio as pf
start = pd.Timestamp('2015-3-1')
rets = pd.read_csv('rets_port.csv', index_col=0, parse_dates=True).loc[start:]
data = (1 + rets).cumprod()

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.models.glyphs import Line
from bokeh.models import Plot, DataRange1d, LinearAxis, ColumnDataSource, Grid, Legend, DatetimeAxis, HoverTool
from bokeh.plotting import figure
from bokeh.session import Session
from bokeh.models.widgets import Slider, TextInput, HBox, VBox, Dialog, CheckboxButtonGroup


document = Document()
session = Session(load_from_config=False)
session.use_doc('interactive')
session.load_document(document)

def update_data():
    global selected, data, rets
    rets['portfolio'] = rets[selected].mean(axis='columns')
    new_data = (1 + rets[selected + ['portfolio']]).cumprod()
    source.data = new_data.reset_index().to_dict('list')
    session.store_document(document)

def on_button_value_change(obj, attr, old, new):
    global selected
    selected = [name for i, name in enumerate(names) if i in new]
    update_data()

data = pd.DataFrame(data)
names = data.drop('portfolio', axis=1).columns.tolist()
data = data.reset_index().to_dict('list')

selected = copy(names)

source = ColumnDataSource(data=data)

colors = sns.color_palette('muted', n_colors=len(names) + 1).as_hex()
p = figure(x_axis_type = "datetime", width=800)#, tools="resize,hover,save")

for color, name in zip(colors, names):
    p.line('index', name, legend=name, name=name, source=source, color=color, line_width=2.)

p.line('index', 'portfolio', legend='portfolio', name='portfolio', source=source, line_width=3., line_dash='dashed', color='red')

p.title = "Cumulative returns"

dialog = Dialog(title="Invalid expression")

checkbox_button_group = CheckboxButtonGroup(
        labels=names, active=list(range(len((names)))))
checkbox_button_group.on_change('active', on_button_value_change)

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('date', '@index'),
])

def create_corr(start, end):
    global rets
    xname = []
    yname = []
    colors = []
    values = []
    names = rets.columns.tolist()
    corr = rets.loc[start:end].corr()
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Correlation matrix
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            xname.append(n1)
            yname.append(n2)
            value = corr.loc[n1, n2]
            values.append(value)
            colors.append(mpl.colors.rgb2hex(cmap(value)))
    return xname, yname, values, colors

latest_dt = rets.index[-1]
month = pd.DateOffset(months=1)

def on_slider_change(obj, attr, old, new):
    global source_corr, session, latest_dt, month
    xname, yname, values, colors = create_corr(latest_dt + (new-1)*month, latest_dt + (new)*month)
    source_corr.data = dict(
            xname=xname,
            yname=yname,
            value=values,
            color=colors
    )
    session.store_document(document)

slider = Slider(start=-10, end=0, value=0, step=1, title="date selection")
slider.on_change('value', on_slider_change)

xname, yname, values, colors = create_corr(latest_dt - month, latest_dt)
source_corr = ColumnDataSource(
        data=dict(
            xname=xname,
            yname=yname,
            value=values,
            color=colors
        )
    )

p_corr = figure(title="Correlations",
    x_axis_location="above", tools="resize,hover,save",
    x_range=list(reversed(names)), y_range=names)
p_corr.plot_width = 800
p_corr.plot_height = 800
p_corr.rect('xname', 'yname', 0.9, 0.9, source=source_corr,
     color='color', line_color=None)

p_corr.grid.grid_line_color = None
p_corr.axis.axis_line_color = None
p_corr.axis.major_tick_line_color = None
p_corr.axis.major_label_text_font_size = "5pt"
p_corr.axis.major_label_standoff = 0
p_corr.xaxis.major_label_orientation = np.pi/3

hover = p_corr.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('names', '@yname, @xname'),
    ('correlation', '@value'),
])

inputs = HBox(children=[checkbox_button_group])
layout = VBox(children=[inputs, p, dialog, p_corr, slider])

document.add(layout)
update_data()

if __name__ == "__main__":
    link = session.object_link(document.context)
    print("Please visit %s to see the plots" % link)
    view(link)
    print("\npress ctrl-C to exit")
    session.poll_document(document)
