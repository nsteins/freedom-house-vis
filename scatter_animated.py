from __future__ import division

import numpy as np
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select, CheckboxGroup, Button
from bokeh.models import Button, Slider, HoverTool, ColumnDataSource
from bokeh.layouts import column,row,widgetbox,layout
from bokeh.palettes import Dark2

def make_data_dict(x_val,y_val,z_val,year):
    df_filter = df[df['Year']==year]
    df_filter = df_filter[df_filter['Region'].isin(
                list(regions[i] for i in region_column.active))]
    df_filter = df_filter[np.isfinite(df_filter[x_val]) & np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]

    x = df_filter[x_val].values
    y = df_filter[y_val].values
    z = df_filter[z_val].values

    MAX_SIZE = 30
    MIN_SIZE = 10
    
    if z_val =='constant':
        size = z*(MIN_SIZE + MAX_SIZE)/2
    elif z!= []:
        size = (z-np.min(z))/(np.max(z)-np.min(z))
        size = MAX_SIZE*size+MIN_SIZE
    else:
        size = []

        

    countries = list(df_filter['Country'].values)    
    color_index = df_filter['Region_code'] 

    data = dict(
                x=x,
                y=y,
                z=z,
                FH = df_filter['Total.Aggr'],
                x_label = [x_column.value]*len(x),
                y_label = [y_column.value]*len(x),
                z_label = [size_column.value]*len(x),
                label=countries,
                size = size,
                color = color_pallette[color_index]
                )

    return data
    
def make_plot():
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value] 
    
    df_filter = df[df['Region'].isin(
                    list(regions[i] for i in region_column.active))]
    df_filter = df_filter[np.isfinite(df_filter[x_val]) & np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]
    years = list(df_filter['Year'].unique())
    
    slider.start = years[0]
    slider.end = years[-1]
    if slider.value not in years:
        slider.value = years[1]
    
    source = ColumnDataSource(data=make_data_dict(x_val,y_val,z_val,slider.value))

    hover = HoverTool()
    hover.tooltips = [
        ("Country", "@label"),
        ("FH Score","@FH"),
        (x_column.value, "@x"),
        (y_column.value,"@y"),
    ]
    
    if z_val != 'constant':
        hover.tooltips.append((size_column.value,"@z"))

    p = figure(width=800,height=700,tools=[hover,'tap'])
    
    p.xaxis.axis_label = x_column.value
    p.yaxis.axis_label = y_column.value
    
    padding = 0.05
    x_pad = (df[x_val].max() - df[x_val].min())*padding
    y_pad = (df[y_val].max() - df[y_val].min())*padding
    p.x_range.start = df[x_val].min() - x_pad
    p.y_range.start = df[y_val].min() - y_pad
    p.x_range.end = df[x_val].max() + x_pad
    p.y_range.end = df[y_val].max() + y_pad


    p.circle('x', 'y', size='size', fill_color='color', line_color='black',
         source=source)
         
    return p,source
    
def update_columns(attr, old, new):
    global plot_source    
    p, plot_source = make_plot()
    lout.children[0] = p

def update_year(attr, old, new):
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value]
    
    plot_source.data.update(make_data_dict(x_val,y_val,z_val,slider.value))
    

def animate_update():
    year = slider.value + 1
    if year > slider.end:
        year = slider.end
        animate()
    slider.value = year


def animate():
    if button.label == '► Play':
        if slider.value == slider.end:
            slider.value = slider.start
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)
        
def reset():
    x_column.value = x_col_init
    y_column.value = y_col_init
    size_column.value = 'constant'
    region_column.active = range(len(regions))
    slider.value = years[0]
       
##Load Data
df = pd.read_csv('data/2006_2015_Master_Data2.csv')
df = df.replace('#REF!',np.nan)
##Load Column Names
column_names = pd.read_csv('data/FH_Col_Names_Desc.csv')
column_names = dict(zip(column_names['Descriptors'].values,column_names['FullNames'].values))

cl = column_names.keys()
drops = ['Year','Country','Region','Status']
cl_clean = list([col for col in cl if col not in drops])
cl_clean = list([col for col in cl_clean if column_names[col] in df.columns])

columns = sorted(cl_clean)
years = list(df['Year'].unique())
regions = list(df['Region'].unique())

#Create region codes for coloring
df['Region_code'] = df['Region'].astype('category').cat.codes
color_pallette = np.array(Dark2[len(df['Region'].unique())])

for col in cl_clean:
    df[column_names[col]] = pd.to_numeric(df[column_names[col]],errors='coerce')

#add constant column for constant bubble size option
df['constant'] = 1
column_names['constant'] = 'constant'
x_col_init = columns[1]
y_col_init = columns[5]

##Create Widgets
button = Button(label='► Play', width=60)
button.on_click(animate)

x_column = Select(title='X-Axis', value=x_col_init, options=columns)
x_column.on_change('value', update_columns)

y_column = Select(title='Y-Axis', value=y_col_init, options=columns)
y_column.on_change('value', update_columns)

size_column = Select(title='Size', value='constant', 
                        options=['constant'] + columns)
size_column.on_change('value', update_columns)

slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
slider.on_change('value', update_year)

region_column = CheckboxGroup(labels=regions[:],active = range(len(regions)))
region_column.on_change('active',update_columns)

reset_button = Button(label = 'Reset')
reset_button.on_click(reset)

#Create initial plot
p, plot_source = make_plot()

controls = widgetbox([x_column, y_column, size_column, region_column,slider,button],width=430)
#top_row = row([controls, p],sizing_mode='scale_width')
#bottom_row = row([slider,button],sizing_mode='scale_both')
#lout = column([top_row,bottom_row],sizing_mode='fixed')
lout = row([p,controls])
curdoc().add_root(lout)
curdoc().title = "FH Scatterplot" 
