import pandas as pd
import numpy as np
import pyfolio as pf

rets = pd.read_csv('rets_contest.csv', index_col=0, parse_dates=True)

import bokeh

from bokeh.charts import Line, TimeSeries, show
from bokeh.models import DatetimeTickFormatter, Glyph

from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.io import output_file, show, vform

from bokeh.models import Callback, ColumnDataSource, BoxSelectTool, Range1d, Rect
from bokeh.plotting import figure, output_file, show

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.models.glyphs import Line
from bokeh.models import Plot, DataRange1d, LinearAxis, ColumnDataSource, Grid, Legend
from bokeh.session import Session
from bokeh.models.widgets import Slider, TextInput, HBox, VBox, Dialog

# prepare some data
document = Document()
session = Session()
session.use_doc('taylor_server')
session.load_document(document)

print(rets)
cum_rets = (1 + rets).cumprod()

#source = ColumnDataSource(data=data)
def on_button_value_change(obj, attr, old, new):
    print(obj, attr, old, new)
    global order
    order = int(new)
    update_data()

# output to static HTML file
#output_file("lines.html", title="line plot example")
# create a new line chat with a title and axis labels
p = TimeSeries(cum_rets, title="Live performance", xlabel='Date',
               ylabel='Cumulative returns (in %)', legend=True,
               width=700, height=400)
lines = p.select(Glyph)
l = lines[1]
l.line_width = 3.
l.line_dash = 'dashed'
print(l.y)

checkbox_button_group = CheckboxButtonGroup(
        labels=rets.columns.tolist(), active=[1, 1, 1, 1, 1])
checkbox_button_group.on_change('value', on_button_value_change)

#show(vform(checkbox_button_group))

#p.legend()
#show(p)
dialog = Dialog(title="Invalid expression")
layout = VBox(children=[p, checkbox_button_group, dialog])
document.add(layout)

if __name__ == "__main__":
    link = session.object_link(document.context)
    print("Please visit %s to see the plots" % link)
    view(link)
    print("\npress ctrl-C to exit")
    session.poll_document(document)
