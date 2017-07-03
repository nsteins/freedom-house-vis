from __future__ import division

import numpy as np
import pandas as pd
from scipy.stats import linregress
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select, CheckboxGroup, Button, Div
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
                color = color_pallette[color_index])
    return data
                
def make_stats_dict(p,data):
    #add stats analysis of x & y variables
    x, y = [data['x'],data['y']]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    x_med = np.median(x)
    y_med = np.median(y)
    
    x_s, x_e = [p.x_range.start,p.x_range.end]
    y_s = x_s*slope + intercept
    y_e = x_e*slope + intercept

    stats = dict(
                x_range = [x_s,x_e],
                y_range = [p.y_range.start,p.y_range.end],
                line_y = [y_s,y_e],
                slope = [slope]*2,
                R_2 = [r_value**2]*2,
                x_med = [x_med]*2,
                y_med = [y_med]*2
                )

    return stats
    
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
    
    hover = HoverTool(tooltips = [
        ("Country", "@label"),
        ("FH Score","@FH"),
        (x_column.value, "@x"),
        (y_column.value,"@y"),
        ])
    
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
    
    source = ColumnDataSource(data=make_data_dict(x_val,y_val,z_val,slider.value))
    stats = ColumnDataSource(data = make_stats_dict(p,source.data))

    scatter = p.circle('x', 'y', size='size', fill_color='color', fill_alpha=0.5,
                        line_color='black',source=source)

    hover.renderers.append(scatter)
    
    
    #add stats info to plot
    p.line('x_range','line_y',source=stats,line_dash='dashed',line_color='red')
    p.line('x_range','y_med',source=stats,line_dash = 'dotted',line_color='black',
            line_alpha=0.7)
    p.line('x_med','y_range',source=stats,line_dash = 'dotted',line_color='black',
            line_alpha=0.7)

         
    return p,source,stats

def update_stats_box(stats):
    s = stats.data
    stats_text = ''.join(["<b>X-axis median</b>: %.2f</br>" % (s['x_med'][0]),
                "<b>Y-axis median</b>: %.2f</br>" % (s['y_med'][0]),
                "<b>Linear regression slope</b>: %.2f</br>" % (s['slope'][0]),
                "<b>R<sup>2</sup></b>: %.2f"  % (s['R_2'][0])
                ])
    return stats_text
    
def update_desc_box():
    x = column_names_df[column_names_df['Descriptors'] == x_column.value]
    y = column_names_df[column_names_df['Descriptors'] == y_column.value]
    z = column_names_df[column_names_df['Descriptors'] == size_column.value]
    desc_text = ''.join(["<b><a href=%s>%s</a></b>: %s</br>" % (x['Link'].iloc[0],x['Descriptors'].iloc[0],
                                                                x['Score Description'].iloc[0]),
                "<b><a href=%s>%s</a></b>: %s</br>" % (y['Link'].iloc[0],y['Descriptors'].iloc[0],
                                                                y['Score Description'].iloc[0]),
                ])
    if not z.empty:
        desc_text +=  "<b><a href=%s>%s</a></b>: %s</br>" % (z['Link'].iloc[0],z['Descriptors'].iloc[0],
                                                                z['Score Description'].iloc[0])
    return desc_text

def update_columns(attr, old, new):
    global plot_source,stats    
    p, plot_source,stats = make_plot()
    lout.children[0] = p
    stats_box.text = update_stats_box(stats)
    desc_box.text = update_desc_box()

def update_year(attr, old, new):
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value]
    
    plot_source.data.update(make_data_dict(x_val,y_val,z_val,slider.value))
    stats.data.update(make_stats_dict(lout.children[0],plot_source.data))
    stats_box.text = update_stats_box(stats)
    desc_box.text = update_desc_box()

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
column_names_df = pd.read_csv('data/FH_Col_Names_Desc.csv')
column_names = dict(zip(column_names_df['Descriptors'].values,column_names_df['FullNames'].values))

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
p, plot_source, stats = make_plot()

stats_box = Div(text = update_stats_box(stats))
desc_box = Div(text = update_desc_box())

controls = widgetbox([x_column, y_column, size_column, 
                      region_column,slider,button,stats_box,
                      desc_box],width=430)
lout = row([p,controls])
curdoc().add_root(lout)
curdoc().title = "FH Scatterplot" 
