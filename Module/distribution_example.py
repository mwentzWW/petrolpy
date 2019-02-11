#%%
import tkinter.filedialog
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.plotly as plotly
from scipy.stats import lognorm

Tk().withdraw()
filename = askopenfilename()

data = pd.read_excel(filename)
#%%
data

#%%
oil_fit_param = lognorm.fit(data["Cum MBO"])
oil_dist = data["Cum MBO"]
oil_dist.hist();

#%%
oil_dist.plot.density();

#%%
data = [go.Histogram(x=oil_dist, histnorm='probability')]
plotly.iplot(data, filename='normalized histogram')

#%%  
hist_data = [oil_dist]
fig = ff.create_distplot(hist_data, group_labels=['Cum MBO'])
plotly.iplot(fig, filename='Basic Distplot')
