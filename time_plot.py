from __future__ import division

import numpy as np
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select, CheckboxGroup, Button, Div, RangeSlider
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import row,widgetbox
from bokeh.palettes import Dark2
from bokeh.embed import autoload_server


def make_data_dict(y_val,z_val,year_range):
    df_filter = df[df['Year'].between(year_range[0],year_range[1])]
    df_filter = df_filter[df_filter['Region'].isin(
                list(regions[i] for i in region_column.active))]
    df_filter = df_filter[df_filter['Country'].isin(
                list(countries[i] for i in country_column.active))]
    df_filter = df_filter[np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]

    x = df_filter['Year'].values
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

        

    country_list = list(df_filter['Country'].values)    
    color_index = df_filter['Region_code'] 

    data = dict(
                x=x,
                y=y,
                z=z,
                FH = df_filter['Total.Aggr'],
                x_label = ['Year']*len(x),
                y_label = [y_column.value]*len(x),
                z_label = [size_column.value]*len(x),
                label=country_list,
                size = size,
                color = color_pallette[color_index])
   
    x, y, color, country = [],[],[],[]
    g = df_filter.groupby('Country')
    for name, group in g:
        x.append(group['Year'].values)
        y.append(group[y_val].values)
        color.append(color_pallette[group['Region_code'].values[0]])
        country.append(name)
        
    line_data = dict(x=x, y=y, color=color, country=country)

    return data,line_data
                
    
def make_plot():
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value] 
    
    df_filter = df[df['Region'].isin(
                    list(regions[i] for i in region_column.active))]
    df_filter = df_filter[np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]
    years = list(df_filter['Year'].unique())
    
    slider.start = years[0]
    slider.end = years[-1]
    if slider.range[0] not in years:
        slider.range = (years[0],slider.range[1])
    if slider.range[1] not in years:
        slider.range = (slider.range[0],years[-1])
    
    year_range = slider.range    
    hover = HoverTool(tooltips = [
        ("Country", "@label"),
        ("FH Score","@FH"),
        ("Year", "@x"),
        (y_column.value,"@y"),
        ])
    
    hover_line = HoverTool(tooltips = [
        ("Country", "@country")])
        
    
    if z_val != 'constant':
        hover.tooltips.append((size_column.value,"@z"))

    p = figure(width=800,height=700,tools=[hover,hover_line])
    
    p.xaxis.axis_label = "Year"
    p.yaxis.axis_label = y_column.value
    
    padding = 0.05
   #x_pad = (df[x_val].max() - df[x_val].min())*padding
    y_pad = (df[y_val].max() - df[y_val].min())*padding
    #p.x_range.start = df[x_val].min() - x_pad
    p.y_range.start = df[y_val].min() - y_pad
    #p.x_range.end = df[x_val].max() + x_pad
    p.y_range.end = df[y_val].max() + y_pad
    
    sc_data,line_data = make_data_dict(y_val,z_val,year_range)
    sc_source = ColumnDataSource(data=sc_data)
    line_source = ColumnDataSource(data=line_data)

    scatter = p.circle('x', 'y', size='size', fill_color='color', fill_alpha=0.5,
                        line_color='black',source=sc_source)
    hover.renderers.append(scatter)
                  
    line = p.multi_line('x', 'y', line_color='color', hover_line_color='color',
                        line_alpha=0.5, hover_alpha = 1,
                        line_width=2, source=line_source)
                        
    line.hover_glyph.line_width = 4
    
    hover_line.renderers.append(line)

    return p,sc_source,line_source

    
def update_desc_box():
    y = column_names_df[column_names_df['Descriptors'] == y_column.value]
    z = column_names_df[column_names_df['Descriptors'] == size_column.value]
    desc_text = ''.join(["<b><a href=%s>%s</a></b>: %s</br>" % (y['Link'].iloc[0],y['Descriptors'].iloc[0],
                                                                y['Score Description'].iloc[0]),
                ])
    if not z.empty:
        desc_text +=  "<b><a href=%s>%s</a></b>: %s</br>" % (z['Link'].iloc[0],z['Descriptors'].iloc[0],
                                                                z['Score Description'].iloc[0])
    return desc_text

def update_columns(attr, old, new):
    global sc_source, line_source
    p, sc_source, line_source = make_plot()
    lout.children[0] = p
    desc_box.text = update_desc_box()

def update_year(attr, old, new):
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value]
    sc_data,line_data = make_data_dict(y_val,z_val,slider.range)
    sc_source.data.update(sc_data)
    line_source.data.update(line_data)
    desc_box.text = update_desc_box()

        
def reset():
    y_column.value = y_col_init
    size_column.value = 'constant'
    region_column.active = range(len(regions))
    slider.range = (years[0],years[-1])
       
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
countries = list(df['Country'].unique())

#Create region codes for coloring
df['Region_code'] = df['Region'].astype('category').cat.codes
color_pallette = np.array(Dark2[len(df['Region'].unique())])

for col in cl_clean:
    df[column_names[col]] = pd.to_numeric(df[column_names[col]],errors='coerce')

#add constant column for constant bubble size option
df['constant'] = 1
column_names['constant'] = 'constant'
y_col_init = columns[5]

##Create Widgets

y_column = Select(title='Variable', value=y_col_init, options=columns)
y_column.on_change('value', update_columns)

size_column = Select(title='Size', value='constant', 
                        options=['constant'] + columns)
size_column.on_change('value', update_columns)

slider = RangeSlider(start=years[0], end=years[-1],range=(years[0],years[-1]),
                     step=1, title="Years")
slider.on_change('range', update_year)

region_column = CheckboxGroup(labels=regions[:],active = range(len(regions)))
region_column.on_change('active',update_columns)

country_column = CheckboxGroup(labels=countries[:],active = range(10))
country_column.on_change('active',update_columns)


reset_button = Button(label = 'Reset')
reset_button.on_click(reset)

#Create initial plot
p, sc_source, line_source = make_plot()

desc_box = Div(text = update_desc_box())

controls = widgetbox([y_column, size_column,country_column,
                      slider,reset_button,desc_box],width=430)
lout = row([p,controls])
curdoc().add_root(lout)
curdoc().title = "FH Time Plot" 

