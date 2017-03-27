from __future__ import division

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Select, MultiSelect
from bokeh.models import CustomJS, ColumnDataSource, HoverTool
from bokeh.layouts import column,row,widgetbox
from bokeh.palettes import Dark2

##Load Data
df = pd.read_csv('data/2006_2015_Master_Data2.csv')
df = df.replace('#REF!',np.nan)
##Load Column Names
column_names = pd.read_csv('data/FH_Col_Names_Desc.csv')
column_names = dict(zip(column_names['Descriptors'].values,column_names['FullNames'].values))

cl = column_names.keys()
drops = ['Year','Country','Region','Status']
cl_clean = list([col for col in cl if col not in drops])

#Create region codes for coloring
df['Region_code'] = df['Region'].astype('category').cat.codes
color_pallette = np.array(Dark2[len(df['Region'].unique())])

for col in cl_clean:
    df[column_names[col]] = df[column_names[col]].convert_objects(convert_numeric=True)

def plot_scatter():
    MAX_SIZE = 20
    MIN_SIZE = 4
    
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value]

    df_filter = df[df['Year']==float(year_column.value)]
    df_filter = df_filter[df_filter['Region'].isin(region_column.value)]
    df_filter = df_filter[np.isfinite(df_filter[x_val]) & np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]

    x = df_filter[x_val].values
    y = df_filter[y_val].values
    z = df_filter[z_val].values
    size = (z-np.min(z))/(np.max(z)-np.min(z))
    countries = list(df_filter['Country'].values)
    
    color_index = df_filter['Region_code'] 

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
    p.xaxis.axis_label = x_column.value
    p.yaxis.axis_label = y_column.value

    p.circle('x', 'y', size='size', fill_color='color', line_color='black',
             source=source)

    return p
   
def update(attr, old, new):
    layout.children[1] = plot_scatter()


##Create Sliders
columns = cl_clean
years = list(df['Year'].unique().astype(str))
regions = list(df['Region'].unique())


x_column = Select(title='X-Axis', value=columns[0], options=columns)
x_column.on_change('value', update)

y_column = Select(title='Y-Axis', value=columns[3], options=columns)
y_column.on_change('value', update)

size_column = Select(title='Size', value=columns[4], options=columns)
size_column.on_change('value', update)

year_column = Select(title='Year', value=years[-3], options=years)
year_column.on_change('value', update)

region_column = MultiSelect(title='Regions', value=regions[:], options=regions)
region_column.on_change('value',update)

controls = widgetbox([x_column, y_column, size_column, year_column, region_column], width=550)
layout = row(controls, plot_scatter())

curdoc().add_root(layout)
curdoc().title = "FH Scatterplot" 
