#%%

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import Range1d, LinearAxis, HoverTool, DatetimeTickFormatter
from bokeh.layouts import gridplot
from itertools import cycle
import pandas as pd

def plot(df, columns, date=False, date_format="%Y-%m-%d"):
    output_notebook()  # To display the plots in Jupyter Notebook

    color_cycle = cycle(["red", "blue", "green", "orange", "purple", "yellow", "pink", "brown", "gray", "teal", 
                        "navy", "olive", "maroon", "cyan", "magenta", "gold", "lime", "indigo", "silver", "black"])

    figures = []  # List to store the figures

    for cols in columns:
        x = cols[0]
        y = cols[1:]

        # Convert x-axis values to datetime if date is True
        if date:
            df[x] = pd.to_datetime(df[x])

        p = figure(x_axis_label=x)

        primary_y_axis = y[:1]
        p.yaxis.axis_label = " / ".join(primary_y_axis)

        if len(y) > 1:
            secondary_y_axis = y[1:]
            p.extra_y_ranges = {}
            for i, secondary_y_col in enumerate(secondary_y_axis):
                p.extra_y_ranges[f"secondary{i}"] = Range1d(start=df[secondary_y_col].min(), end=df[secondary_y_col].max())
                p.add_layout(LinearAxis(y_range_name=f"secondary{i}", axis_label=secondary_y_col), 'right')

        colors = color_cycle  # Use the color_cycle directly

        for i, y_col in enumerate(y):
            color = next(colors)  # Get the next color from the color_cycle
            if i == 0:
                line = p.line(df[x], df[y_col], legend_label=y_col, color=color)
            else:
                line = p.line(df[x], df[y_col], legend_label=y_col, y_range_name=f"secondary{i-1}", color=color)

            # Add HoverTool to each line
            tooltips = [(x, f"@{{{x}}}"), (y_col, f"@{{{y_col}}}")]

            hover = HoverTool(renderers=[line], tooltips=tooltips)
            p.add_tools(hover)

        if date:
            p.xaxis.formatter = DatetimeTickFormatter(seconds=date_format)

        p.legend.location = "top_left"

        figures.append(p)  # Add the figure to the list

    # Create a grid of figures
    grid = gridplot(figures, ncols=2)  # Adjust the number of columns as needed

    show(grid)




#%%
import numpy as np

x = np.linspace(-3*np.pi,3*np.pi,50)
cosin = np.cos(x)*0.5 
sinus = np.sin(x)
timestamps = pd.date_range(start='2022-01-01', periods=50, freq='H')
formatted_timestamps = timestamps.strftime("%Y-%m-%d %H:%M:%S")

# %%
import pandas as pd
test_df = pd.DataFrame({"rad": x, "cos": cosin, "sin": sinus, "date": timestamps})
# %%

plot(test_df, [["rad", "cos"], ["rad", "sin"],["rad", "sin","cos"]],date = False)
plot(test_df,[["date","cos"],["date","sin"],["date","sin","cos"]],date = True,date_format="%Y-%m-%d %H:%M:%S")
# %%
