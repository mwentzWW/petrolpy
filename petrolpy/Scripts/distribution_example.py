#%%
import math
import numpy as np
import pandas as pd
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

data = pd.read_csv("https://raw.githubusercontent.com/mwentzWW/petrolpy/master/petrolpy/Test_Data/EUR_Data.csv")
#%%
data

#%%
# lognorm.fit returns (shape, floc, scale)
# shape is sigma or the standard deviation, scale = exp(mean)
sigma, floc, scale  = lognorm.fit(data["CUM_MBO"], floc=0)
mu = math.log(scale)
oil_dist = data["CUM_MBO"]
oil_dist.hist()
#%%
hist, edges = np.histogram(data["CUM_MBO"], density=True, bins=100)

x = np.linspace(0.0001, np.max(oil_dist) + np.mean(oil_dist), 1000)
pdf = 1/(x* sigma * np.sqrt(2*np.pi)) * np.exp(-(np.log(x)-mu)**2 / (2*sigma**2))
cdf = (1+scipy.special.erf((np.log(x)-mu)/(np.sqrt(2)*sigma)))/2

plot_1 = make_plot("Log Normal Distribution (μ={}, σ={})".format(round(scale, 2),round(sigma, 2)), hist, edges, x, pdf, cdf)
show(plot_1)
#%%
# Find P10, P50, and P90
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return (array[idx], idx)

p50_param = find_nearest(cdf, 0.5)
p50_param