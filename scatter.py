from __future__ import division

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Select
from bokeh.models import CustomJS, ColumnDataSource, HoverTool
from bokeh.layouts import column,row,widgetbox
from bokeh.palettes import Dark2

##Load Data
df = pd.read_csv('data/joined_data.csv')

def plot_scatter():
    MAX_SIZE = 20
    MIN_SIZE = 4
    
    df_filter = df[np.isfinite(df[x_column.value]) & np.isfinite(df[y_column.value]) & np.isfinite(df[size_column.value])]

    x = df_filter[x_column.value].values
    y = df_filter[y_column.value].values
    z = df_filter[size_column.value].values
    size = (z-np.min(z))/(np.max(z)-np.min(z))
    countries = list(df_filter['Country.Territory'].values)
    
    regions = df_filter['Region.x']
    color_pallette = np.array(Dark2[len(regions.unique())])
    color_index = regions.astype('category').cat.codes.values

    source = ColumnDataSource(
        data=dict(
            x=x,
            y=y,
            z=z,
            label=countries,
            size = MAX_SIZE*size+MIN_SIZE,
            color = color_pallette[color_index]
        )
    )
    

    hover = HoverTool()
    hover.tooltips = [
        ("Country", "@label"),
        (x_column.value, "@x"),
        (y_column.value,"@y"),
        (size_column.value,"@z")
    ]

    p = figure(plot_width=900, plot_height=600,tools=[hover])

    p.circle('x', 'y', size='size', fill_color='color', line_color='black',
             source=source)

    return p
   
def update(attr, old, new):
    layout.children[1] = plot_scatter()


##Create Sliders
columns = ['CL.Aggr','PR.Aggr','Total.Aggr','FSI_Total','TI_CPI2015','unhdi.Human.Development.Index..HDI.']

x_column = Select(title='X-Axis', value=columns[0], options=columns)
x_column.on_change('value', update)

y_column = Select(title='Y-Axis', value=columns[3], options=columns)
y_column.on_change('value', update)

size_column = Select(title='Size', value=columns[4], options=columns)
size_column.on_change('value', update)

controls = widgetbox([x_column, y_column, size_column], width=300)
layout = row(controls, plot_scatter())

curdoc().add_root(layout)
curdoc().title = "FH Scatterplot" 
