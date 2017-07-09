from __future__ import division

import numpy as np
import pandas as pd
from scipy.stats import linregress
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select, CheckboxGroup,  Div
from bokeh.models import Button, Slider, HoverTool, ColumnDataSource
from bokeh.layouts import row,widgetbox
from bokeh.palettes import Dark2
from bokeh.embed import autoload_server

#This function will create a dictionary of the scatterplot data to be used as
#the source for the scatter plot. The dictionary contains both the data and the 
#information necessary for the hover tool labels.
#
#INPUTS: x_val - column name of the variable to be used on the x-axis
#y_val - column name of the variable to be used on the y-axis
#z_val - column name of the variable to be used for the point size
#year - The year to use data from
#
#RETURNS: data - dictionary containing data used for the scatter plot and hover
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

#This function creates a data dictionary that is used for plotting the stats
#data. Median values and least squares linear fit are calculated and then the 
#values that will be used to add to the plot are returned in a dictionary. This
#function must have access to the figure object so that it can give the correct
#boundary values to 'make_plot()'.
#
#INPUTS: p - the Bokeh figure that the stats data will be added to
# data - the data dictionary that the stats should be computed from
#
#RETURNS: stats - a dictionary containing the values needed for adding stats
#info to the plot
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

#This function creates the scatter plot for the application.
#make_plot does not take any inputs, but checks the state of the control widgets
#in order to determine which values to plot.
#
#RETURNS: p -  the bokeh figure object containing the plot
#source - the bokeh ColumnDataSource containing the scatter plot data
#stats - the bokeh ColumnDataSource containing the stats data  
def make_plot():
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value] 
    
    #filter dataframe based on selected regions and make sure all columns have valid data
    df_filter = df[df['Region'].isin(
                    list(regions[i] for i in region_column.active))]
    df_filter = df_filter[np.isfinite(df_filter[x_val]) & np.isfinite(df_filter[y_val]) & np.isfinite(df_filter[z_val])]
    
    #Adjust the slider so it only points to years where the data is valid
    years = list(df_filter['Year'].unique())
    slider.start = years[0]
    slider.end = years[-1]
    if slider.value not in years:
        slider.value = years[1]
    
    #Define the Hovertool properties
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
    
    #add axis padding
    padding = 0.05
    x_pad = (df[x_val].max() - df[x_val].min())*padding
    y_pad = (df[y_val].max() - df[y_val].min())*padding
    p.x_range.start = df[x_val].min() - x_pad
    p.y_range.start = df[y_val].min() - y_pad
    p.x_range.end = df[x_val].max() + x_pad
    p.y_range.end = df[y_val].max() + y_pad
    
    #Create ColumnDataSources from dictionaries
    source = ColumnDataSource(data = make_data_dict(x_val,y_val,z_val,slider.value))
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

#This function takes a stats dictionary and creates an HTML formatted string
#containing the interesting values so they can be displayed in a Div box.
#
#INPUT: stats - a dictionary containing stats info as created by make_stats_dict
#RETURNS: stats_text - HTML formatted string containing stats descriptions
def update_stats_box(stats):
    s = stats.data
    stats_text = ''.join(["<b>X-axis median</b>: %.2f</br>" % (s['x_med'][0]),
                "<b>Y-axis median</b>: %.2f</br>" % (s['y_med'][0]),
                "<b>Linear regression slope</b>: %.2f</br>" % (s['slope'][0]),
                "<b>R<sup>2</sup></b>: %.2f"  % (s['R_2'][0])
                ])
    return stats_text

#This function looks up the descriptions of the selected column values from a 
#dataframe that was loaded from 'data/FH_Col_Names_Desc.csv'. This data is then 
#formatted into an HTML string
#
#RETURNS: desc_text - HTML formatted string containing column descriptions
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

#This function is called whenever the value of any of the column drop down options
#are changed. This function creates a new plot object by calling 'make_plot'
#and replaces the old plot in the layout with the new plot. The stats and 
#description information is also updated
def update_columns(attr, old, new):
    global plot_source,stats    
    p, plot_source,stats = make_plot()
    lout.children[0] = p
    stats_box.text = update_stats_box(stats)
    desc_box.text = update_desc_box()

#This function is called whenever the value of the year slider is changed.
#In order to make the animation smooth, the plot object is not replaced,
#instead, the plot_source is updated with a new data dictionary from 
#make_data_dict. The stats and description information is also updated
def update_year(attr, old, new):
    x_val = column_names[x_column.value]
    y_val = column_names[y_column.value]
    z_val = column_names[size_column.value]
    
    plot_source.data.update(make_data_dict(x_val,y_val,z_val,slider.value))
    stats.data.update(make_stats_dict(lout.children[0],plot_source.data))
    stats_box.text = update_stats_box(stats)
    desc_box.text = update_desc_box()

#This is called by the 'animate' function
#This increments the slider value by one until it is at the end value
#This change in the slider value auto-triggers 'update_year'
def animate_update():
    year = slider.value + 1
    if year > slider.end:
        year = slider.end
        animate()
    slider.value = year

#This is called when the 'Play' button is pressed
#This calls 'animate_update' and then waits for 500ms before calling again
def animate():
    if button.label == '► Play':
        if slider.value == slider.end:
            slider.value = slider.start
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)

#This is called when the 'Reset' button is pressed
#Resets all widget values to their default value        
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


stats_box = Div(text = update_stats_box(stats))
desc_box = Div(text = update_desc_box())


#Create initial plot
p, plot_source, stats = make_plot()

#Add Plot and Widgets to document layout
controls = widgetbox([x_column, y_column, size_column, 
                      region_column,slider,button,reset_button
                      ,stats_box,desc_box],width=430)
lout = row([p,controls])
curdoc().add_root(lout)
curdoc().title = "FH Scatterplot" 

#Export script for embedding plot in other pages
with open('scatter_animated_embed.html','w') as f:
    script = autoload_server(url = "https://fh-vis.herokuapp.com/scatter_animated")
    f.write(script)