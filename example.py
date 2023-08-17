
#%%
from coplotter import multiPlot
import numpy as np
#%%
import pandas as pd
x = np.linspace(-3*np.pi,3*np.pi,50)
cosin = np.cos(x)*0.5 
sinus = np.sin(x)
timestamps = pd.date_range(start='2022-01-01', periods=50, freq='H')
formatted_timestamps = timestamps.strftime("%Y-%m-%d %H:%M:%S")

# %%
test_df = pd.DataFrame({"rad": x, "cos": cosin, "sin": sinus, "date": formatted_timestamps})

# %%
multiPlot(test_df, [["rad", "cos"], ["rad", "sin"],["rad", "sin","cos"]],date = False)
multiPlot(test_df,[["date","cos"],["date","sin"],["date","sin","cos"]],date = True,date_format="%Y-%m-%d %H:%M:%S")


# %%
