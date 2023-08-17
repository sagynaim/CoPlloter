#%%
import numpy as np
import pandas as pd
from coplotter import multiPlot

#%%
x = np.linspace(-3*np.pi,3*np.pi,50)
cosin = np.cos(x)*0.5 
sinus = np.sin(x)
timestamps = pd.date_range(start='2022-01-01', periods=50, freq='H')
formatted_timestamps = timestamps.strftime("%Y-%m-%d %H:%M:%S")

# %%
test_df = pd.DataFrame({"rad": x, "cos": cosin, "sin": sinus, "date": formatted_timestamps, "date_2": formatted_timestamps})
time_test_df = pd.DataFrame({"date": formatted_timestamps, "date_2": formatted_timestamps})
# %%

multiPlot(test_df,chart_type="bar",columns = [["rad", "cos"], ["rad", "sin"],["rad", "sin","cos"]],date = False)
multiPlot(test_df,[["date","cos"],["date","sin"],["date","sin","cos"],["date","sin","cos"],["date","sin","cos"],["date","sin","cos"]],date = 'x',date_format="%Y-%m-%d %H:%M:%S")
multiPlot(time_test_df,[["date","date_2"]],date = 'xy',date_format="%Y-%m-%d %H:%M:%S")

# %%

