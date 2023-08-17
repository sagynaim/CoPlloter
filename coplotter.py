
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import Range1d, LinearAxis, HoverTool, DatetimeTickFormatter
from bokeh.layouts import gridplot
from itertools import cycle


def _generateScatter(figure, df, x_values, column, index, color):

    DEFAULT_MARKER_SIZE = 3
    MAX_MARKER_SIZE = 30
    
    num_points = len(df[x_values])
    marker_size = DEFAULT_MARKER_SIZE + (MAX_MARKER_SIZE - DEFAULT_MARKER_SIZE) * (num_points - 1) / (100 - 1)
    
    if index == 0:
        
        figure.circle(df[x_values], df[column], legend_label=column, color=color, size=marker_size)
        
    else:
        
        figure.circle(df[x_values], df[column], legend_label=column, y_range_name=f"secondary{index-1}", color=color, size =marker_size)                

def _generateLine(figure, df, x_values, column, index, color):
    
    if index == 0:
        
        figure.line(df[x_values], df[column], legend_label=column, color=color)
        
    else:
        
        figure.line(df[x_values], df[column], legend_label=column, y_range_name=f"secondary{index-1}", color=color)


def _generateBar(figure, df, x_values, column, color):
    
    bar_width = 5 / len(df[x_values])  # Adjust the bar width based on the number of x-axis values
    figure.vbar(x=df[x_values], top=df[column], legend_label=column, width=bar_width, color=color)
    
def _addSecondaryAxis(figure, df, y):
    
    secondary_y_axis = y[1:]
    figure.extra_y_ranges = {}
    start = min(df[secondary_y_col].min() for secondary_y_col in secondary_y_axis)
    end = max(df[secondary_y_col].max() for secondary_y_col in secondary_y_axis)
    for i, secondary_y_col in enumerate(secondary_y_axis):
        
        figure.extra_y_ranges[f"secondary{i}"] = Range1d(start=start, end=end)
        figure.add_layout(LinearAxis(y_range_name=f"secondary{i}", axis_label=secondary_y_col), 'right')

def _generateHoverTool(chart_type, date, date_format="%Y-%m-%d"):
    
    x_format = '@x'
    y_format = '@y'
    
    if chart_type == "bar":
        y_format = '@top'

    elif chart_type == "line" or chart_type == "scatter":
        y_format = '@y'
        
    if date =='x': 
        
        x_format = '@x{%s}' % date_format
        tooltips =[
            ('Date',x_format ),
            ('Value', y_format)
        ]
        hover_tool = HoverTool(tooltips=tooltips, formatters={'@x': 'datetime'}, mode='vline')
        return hover_tool
    
    elif date =='y': 
        y_format = '@y{%s}' % date_format
        tooltips =[
            ('X',x_format ),
            ('Date', y_format)
        ]
        hover_tool = HoverTool(tooltips=tooltips, formatters={'@y': 'datetime'}, mode='vline')
        return hover_tool
    elif date =='xy': 
        x_format = '@x{%s}' % date_format
        y_format = '@y{%s}' % date_format
        tooltips =[
            ('Date',x_format ),
            ('Y_Date', y_format)
        ]  
        hover_tool = HoverTool(tooltips=tooltips, formatters={'@y': 'datetime', '@x': 'datetime'}, mode='vline')
        return hover_tool
    else: 
        tooltips =[
            ('X',x_format ),
            ('Y', y_format)
        ]     
        hover_tool = HoverTool(tooltips=tooltips, mode='vline')
        return hover_tool

def multiPlot(df, columns, chart_type="line", date=False, date_format="%Y-%m-%d"):
    from bokeh.io import output_notebook

    #output_notebook()  # To display the plots in Jupyter Notebook

    
    figures = []  # List to store the figures
    color_cycle = cycle(["red", "blue", "green", "orange", "purple", "yellow", "pink", "brown", "gray", "teal", "navy", "olive", "maroon", "cyan", "magenta", "gold", "lime", "indigo", "silver", "black"])
    
    for cols in columns:
        
        x_values = cols[0]
        y_values = cols[1:]
       
        # Convert x/y-axis values to datetime 
        if date == 'x': df[x_values] = pd.to_datetime(df[x_values], format=date_format, errors='coerce')        
        elif date == 'y': 
            for col in y_values:
                df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
        elif date == 'xy':
            df[x_values] = pd.to_datetime(df[x_values], format=date_format, errors='coerce')
            for col in y_values:
                df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')            
        fig = figure(x_axis_label=x_values)
        primary_y_axis = y_values[:1]
        fig.yaxis.axis_label = " / ".join(primary_y_axis)
        if len(y_values) > 1 and chart_type != "bar":
            
            _addSecondaryAxis(fig, df, y_values)
            
        for index, y_col in enumerate(y_values):
            color = next(color_cycle)  # Get the next color from the color_cycle
            if chart_type == "line":
                
                _generateLine(fig, df, x_values, y_col, index, color)
                    
            elif chart_type == "bar":
                
                _generateBar(fig, df, x_values, y_col, color)
                
            elif chart_type == "scatter":
                
                _generateScatter(fig, df, x_values, y_col, index, color)
            else:
                
                raise ValueError("Invalid chart_type. Supported values are 'line', 'bar', and 'scatter'.")

        if date == 'x': fig.xaxis.formatter = DatetimeTickFormatter()
        elif date == 'y': fig.yaxis.formatter = DatetimeTickFormatter() 
        elif date == 'xy':
            fig.xaxis.formatter = DatetimeTickFormatter()
            fig.yaxis.formatter = DatetimeTickFormatter()
        elif date == False: pass
        else: raise ValueError("Invalid date parameter. Supported values are 'x' and 'y' or False.")   
        
        fig.legend.location = "top_left"
        fig.add_tools(_generateHoverTool(chart_type, date, date_format))
        figures.append(fig)  # Add the figure to the list

    grid = gridplot(figures, ncols=2)  # Adjust the number of columns as needed
    show(grid)




