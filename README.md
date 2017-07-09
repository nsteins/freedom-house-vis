# freedom-house-vis
Visualizing Freedom House Data

This a collection of interactive web plots for visualizing the relationships between [Freedom House](https://freedomhouse.org/) scores and other socio-economic indicators, including the Fragile States Index, UN Human Development Index and World Bank open data. This application was developed by volunteers working with [DataKind - DC](http://www.datakind.org/chapters/datakind-dc)

## Running the applications
This repository already contains the necessary `requirements.txt` and `ProcFile` to run on a [Heroku](https://heroku.com) dyno, simply by cloning this program and deploying it to Heroku. 

To run the applications locally, you must use the bokeh server command. Do this by entering the directory containing the files and running

```bokeh serve --show time_plot.py scatter_animated.py```

## Data description
Data for the plots are stored in `2006_2015_Master_Data2.csv`, where each row contains the data for a single country or
territory during a single year.

The columns that are used in the plot are stored in `FH_Col_Names_Desc.csv`. This contains several columns which include
the name of the columns from `2006_2015_Master_Data2.csv`, a description, the source of the data, a link to an external
site describing the dataset, and a summary of the meaning of the column values.
