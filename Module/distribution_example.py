#%%
import tkinter.filedialog
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.plotly as plotly
import scipy.special
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from scipy.stats import lognorm


def make_plot(title, hist, edges, x, pdf, cdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

Tk().withdraw()
filename = askopenfilename()

data = pd.read_excel(filename)
#%%
data

#%%
# lognorm.fit returns (shape, floc, scale)
# shape is sigma or the standard deviation, scale = mean??
# the loc is shifting the plot left or right??
sigma, floc, mu  = lognorm.fit(data["Cum MBO"], floc=0)
oil_dist = data["Cum MBO"]
oil_dist.hist();
#%%
hist, edges = np.histogram(data["Cum MBO"], density=True, bins=50)

x = np.linspace(0.0001, 8.0, 1000)
pdf = 1/(x* sigma * np.sqrt(2*np.pi)) * np.exp(-(np.log(x)-mu)**2 / (2*sigma**2))
cdf = (1+scipy.special.erf((np.log(x)-mu)/(np.sqrt(2)*sigma)))/2

plot_1 = make_plot("Log Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf, cdf)
show(plot_1)
#%%
oil_dist.plot.density();

#%%
data = [go.Histogram(x=oil_dist, histnorm='probability')]
offline.iplot(data, filename='normalized histogram')

#%%  
hist_data = [oil_dist]
fig = ff.create_distplot(hist_data, group_labels=['Cum MBO'])
offline.iplot(fig, filename='Basic Distplot')
