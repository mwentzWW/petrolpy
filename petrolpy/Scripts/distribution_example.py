# %%
import math

import numpy as np
import pandas as pd
import scipy.special
from bokeh.layouts import gridplot
from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, HoverTool, ColumnDataSource, PrintfTickFormatter
from scipy.stats import lognorm, norm
# %%
# Bokeh output to notebook setting
# output_notebook()
# %%
# Find P10, P50, and P90


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return (array[idx], idx)


def make_plot_cdf(title, hist, edges, x, pdf, cdf, x_label):
    p = figure(title=title, background_fill_color="#fafafa", x_axis_type='log')
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

    p.x_range.start = 1
    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color = "white"
    p.left[0].formatter.use_scientific = False

    return p


def make_plot_probit(title, input_data, x_label):
    '''Creates Probit plot for EUR and data that has a log-normal distribution.
    '''
    # Calculate log-normal distribtion for input data
    sigma, floc, scale = lognorm.fit(input_data, floc=0)
    mu = math.log(scale)
    x = np.linspace(0.001, np.max(input_data) + np.mean(input_data), 1000)
    pdf = 1/(x * sigma * np.sqrt(2*np.pi)) * \
        np.exp(-(np.log(x)-mu)**2 / (2*sigma**2))
    cdf = (1+scipy.special.erf((np.log(x)-mu)/(np.sqrt(2)*sigma)))/2

    p = figure(title=title, background_fill_color="#fafafa", x_axis_type='log')

    # Prepare input data for plot
    input_data_log = np.log(input_data)
    # Get percentile of each point by getting rank/len(data)
    input_data_log_sorted = np.argsort(input_data_log)
    ranks = np.empty_like(input_data_log_sorted)
    ranks[input_data_log_sorted] = np.arange(len(input_data_log))
    
    input_data_log_perc = [(x + 1)/(len(input_data_log_sorted))
                           for x in ranks]
    input_data_y_values = norm._ppf(input_data_log_perc)

    # Prepare fitted line for plot
    x_y_values = norm._ppf(cdf)

    # Values to display on y axis instead of z values from ppf
    y_axis = [1 - x for x in cdf]

    # Plot input data values
    p.scatter(input_data, input_data_y_values, size=15,
              line_color="navy", legend="Input Data", marker='circle_cross')
    p.line(x, x_y_values, line_width=3, line_color="red", legend="Best Fit")

    # calculate P90, P50, P10
    p10_param = find_nearest(cdf, 0.9)
    p10 = round(x[p10_param[1]])
    p50_param = find_nearest(cdf, 0.5)
    p50 = round(x[p50_param[1]])
    p90_param = find_nearest(cdf, 0.1)
    p90 = round(x[p90_param[1]])

    # Add P90, P50, P10 markers
    p.scatter(p90, norm._ppf(0.10), size=20, line_color="black",
              fill_color='darkred', legend='P90', marker='square_x')
    p.scatter(p50, norm._ppf(0.50), size=20, line_color="black",
              fill_color='blue', legend='P50', marker='square_x')
    p.scatter(p10, norm._ppf(0.90), size=20, line_color="black",
              fill_color='red', legend='P10', marker='square_x')

    # Add P90, P50, P10 segments
   # p.segment(1, norm._ppf(0.10), np.max(x), norm._ppf(0.10), line_dash='dashed', line_width=2, line_color='black', legend="P90")
   # p.segment(1, norm._ppf(0.50), np.max(x), norm._ppf(0.50), line_dash='dashed', line_width=2, line_color='black', legend="P50")
   # p.segment(1, norm._ppf(0.90), np.max(x), norm._ppf(0.90), line_dash='dashed', line_width=2, line_color='black', legend="P10")
    p.segment(p90, -4, p90, np.max(x_y_values), line_dash='dashed',
              line_width=2, line_color='darkred', legend="P90")
    p.segment(p50, -4, p50, np.max(x_y_values), line_dash='dashed',
              line_width=2, line_color='blue', legend="P50")
    p.segment(p10, -4, p10, np.max(x_y_values), line_dash='dashed',
              line_width=2, line_color='red', legend="P10")

    # Plot Styling
    p.x_range.start = 1
    p.y_range.start = -3
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = 'Z'
    p.left[0].formatter.use_scientific = False
    p.xaxis[0].formatter = PrintfTickFormatter(format="%i")
    p.yaxis.visible = False
    p.title.text = title + \
        " & (P90: {}, P50: {}, P10: {})".format(int(p90), int(p50), int(p10))
    p.title.align = 'center'
    p.legend.click_policy = "mute"

    return p


def make_plot_pdf(title, hist, edges, x, pdf, x_label):
        
    source = ColumnDataSource(data = {
        'x' : x,
        'pdf': pdf,
    })

    p = figure(background_fill_color="#fafafa", )
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line('x', 'pdf', line_color="black", line_width=4, alpha=0.8, legend="PDF",
           hover_alpha=0.4, hover_line_color="black", source=source)

    # calculate P90, P50, P10
    p10_param = find_nearest(cdf, 0.9)
    p10 = round(x[p10_param[1]])
    p50_param = find_nearest(cdf, 0.5)
    p50 = round(x[p50_param[1]])
    p90_param = find_nearest(cdf, 0.1)
    p90 = round(x[p90_param[1]])

    p.line((p90, p90), [0, np.max(pdf)],
           line_color='darkred', line_width=3, legend="P90")
    p.line((p50, p50), [0, np.max(pdf)],
           line_color='blue', line_width=3, legend="P50")
    p.line((p10, p10), [0, np.max(pdf)],
           line_color='red', line_width=3, legend="P10")

    lower = BoxAnnotation(left=p90, right=p50,
                          fill_alpha=0.1, fill_color='darkred')
    middle = BoxAnnotation(left=p50, right=p10,
                           fill_alpha=0.1, fill_color='blue')
    upper = BoxAnnotation(
        left=p10, right=x[-1], fill_alpha=0.1, fill_color='darkred')
    
    # Hover Tool
    p.add_tools(HoverTool(
    tooltips=[
        ( x_label, '@x{f}'            ),
        ( 'Probability', '@pdf{%0.6Ff}' ), # use @{ } for field names with spaces
    ]))

    # Plot Styling
    p.add_layout(lower)
    p.add_layout(middle)
    p.add_layout(upper)
    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color = "white"
    p.left[0].formatter.use_scientific = False
    p.xaxis[0].formatter.use_scientific = False
    p.title.text = title + \
        " & (P90: {}, P50: {}, P10: {})".format(int(p90), int(p50), int(p10))
    p.title.align = 'center'

    return p


# %%
data = pd.read_csv(
    "https://raw.githubusercontent.com/mwentzWW/petrolpy/master/petrolpy/Test_Data/EUR_Data.csv")
# %%
data
input_data = data["CUM_MBO"]
# %%
# lognorm.fit returns (shape, floc, scale)
# shape is sigma or the standard deviation, scale = exp(median)
sigma, floc, scale = lognorm.fit(input_data, floc=0)
mu = math.log(scale)
# %%
hist, edges = np.histogram(input_data, density=True, bins='auto')

x = np.linspace(0.001, np.max(input_data) + np.mean(input_data), 1000)
pdf = 1/(x * sigma * np.sqrt(2*np.pi)) * \
    np.exp(-(np.log(x)-mu)**2 / (2*sigma**2))
cdf = (1+scipy.special.erf((np.log(x)-mu)/(np.sqrt(2)*sigma)))/2
mean = np.exp(mu + 0.5*(sigma**2))
# %%
plot_cdf = make_plot_cdf("Log Normal Distribution (n= {}, mean={}, σ={})".format(round(len(
    input_data), 2), round(mean), round(sigma, 2)), hist, edges, x, pdf, cdf, 'Cum MBO')
plot_pdf = make_plot_pdf("Log Normal Distribution (n= {}, mean={}, σ={})".format(round(
    len(input_data), 2), round(mean), round(sigma, 2)), hist, edges, x, pdf, 'Cum MBO')
plot_dist = make_plot_probit("Log Normal Distribution (n= {}, mean={}, σ={})".format(
    round(len(input_data), 2), round(mean), round(sigma, 2)), input_data, 'Cum MBO')
# %%
show(plot_cdf)
# %%
show(plot_pdf)
# %%
show(plot_dist)
# %%
# P50 value
p50_param = find_nearest(cdf, 0.5)
p50_value = round(x[p50_param[1]])
p50_value
# %%
# P10 value, only 10% of values will have this value or more
p10_param = find_nearest(cdf, 0.9)
p10_value = round(x[p10_param[1]])
p10_value
# %%
# P90 value, 90% of values will have this value or more
p90_param = find_nearest(cdf, 0.1)
p90_value = round(x[p90_param[1]])
p90_value
# %%
