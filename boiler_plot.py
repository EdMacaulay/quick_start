#############################################################################################
# boiler plot
# ed macaulay
# edward.macaulay@gmail.com
#############################################################################################
#It's quick and easy to make plots in python, but
#it takes more work to get a plot ready for publication.
#This script includes most of the 'boiler plate' code
#that is needed.
#############################################################################################
# import libraries
#############################################################################################

import os # for making directories
import math # for basic math
import numpy as np # for handling arrays
import matplotlib.pyplot as plt # for plotting

#############################################################################################
# define arbitrary function, just to generate some data to plot
#############################################################################################

def arbitrary_function(x):
    y = 10.0 + x**(-1.0) + x**(2.0)
    return y

#############################################################################################
# generate and save data to plot
# this is just so that we have some data to plot
# you wil not usually have this
#############################################################################################

x_min = 0.01
x_max = 100.0
N_points = 100
delta_scale = 5.0

x_line = np.logspace(math.log10(x_min),math.log10(x_max),num=N_points,base=10)
y_line = arbitrary_function(x_line)
y_delta = np.random.normal(loc=0.0, scale=delta_scale, size=N_points) # add in some scatter
y_data = y_line + y_delta
y_error = np.random.normal(loc=0.0, scale=delta_scale, size=N_points) # generate some errors

data_block = np.array([x_line,y_line,y_data,y_error])
data_block = data_block.T

data_path = 'boiler_data'
data_tag = 'generated_data'
data_suffix = '.csv'
data_name = data_path + '/' + data_tag + data_suffix

if os.path.isdir(data_path):
    print 'Data path ok'
else:
    os.mkdir(data_path)

np.savetxt( data_name , data_block , delimiter=',')

#############################################################################################
# load data
#############################################################################################

data_block = np.loadtxt( data_name , delimiter=',' )
x_line  = data_block[:,0]
y_line  = data_block[:,1]
y_data  = data_block[:,2]
y_error = data_block[:,3]

#############################################################################################
# define colors and settings
#############################################################################################

color_red = '#d50000'
color_pink='#c51162'
color_purple='#aa00ff'
color_indigo='#6200ea'
color_blue='#304ffe'
color_teal='#00bfa5'
color_green='#00c853'

font_size_ticks = 12
font_size_labels = 18

line_width =1
fill_alpha = 0.5
line_alpha = 0.9

theory_color = 'indigo'
data_color='black'
data_line = 'none'
data_marker = 'h'
data_point_size = 3

#############################################################################################
# setup plot to look nice
#############################################################################################

plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=font_size_ticks)
plt.rc('ytick', labelsize=font_size_ticks)

#############################################################################################
# setup subplots
#############################################################################################

plt.subplot(2,1,1)

plt.ylabel(r'$\rm{Residual,}$ $\Delta_y$',fontsize=font_size_labels, labelpad=8)

plt.axhline(y=0,c='black', lw =line_width, alpha = line_alpha   )
plt.semilogx(x_line, y_delta,c=data_color,lw=line_width, ls=data_line,marker=data_marker,ms=data_point_size, alpha=line_alpha )

# plot a filled region
limit_scale = np.mean(abs(y_error))
y_hi_1 = limit_scale
y_hi_2 = 2.0 * limit_scale
y_lo_1 = -limit_scale
y_lo_2 = -2.0 * limit_scale
plt.fill_between(x_line, y_lo_2, y_hi_2, facecolor=color_indigo, edgecolor='none' , interpolate=True,alpha=fill_alpha)
plt.fill_between(x_line, y_lo_1, y_hi_1, facecolor=color_indigo, edgecolor='none' , interpolate=True,alpha=fill_alpha)

# plot error bars
plt.errorbar(x_line, y_delta, yerr = y_error , capsize=0 , lw=line_width ,c=data_color,ls=data_line,marker=data_marker,ms=data_point_size , alpha=line_alpha )

# more plot settings
plt.xlim([x_min, x_max])
plt.setp(plt.gcf().get_axes(), xticks=[]) # turn off ticks on x-axis for subplot

#############################################################################################
# next subplot
#############################################################################################

plt.subplot(2,1,2)

# axis labels
plt.xlabel(r'$\rm{Describe,}$ $x$ $\rm{[Units]}$',fontsize=font_size_labels, labelpad=4)
plt.ylabel(r'$\rm{Describe,}$ $y$ $\rm{[Units]}$',fontsize=font_size_labels, labelpad=4)
plt.xlim([x_min, x_max])

# actually plot things here
plt.loglog(x_line, y_line, c='black',alpha=line_alpha , lw=line_width)

Theory_B = y_line/x_line
plt.loglog(x_line, Theory_B , c='black',alpha=line_alpha , lw=line_width, ls='--')

# plot a filled region
y_hi_1 = y_line + limit_scale
y_hi_2 = y_line + 2.0 * limit_scale
y_lo_1 = y_line + -limit_scale
y_lo_2 = y_line + -2.0 * limit_scale

plt.fill_between(x_line, y_lo_2, y_hi_2, facecolor=color_indigo, edgecolor='none' , interpolate=True,alpha=fill_alpha)
plt.fill_between(x_line, y_lo_1, y_hi_1, facecolor=color_indigo, edgecolor='none' , interpolate=True,alpha=fill_alpha)

# plot error bars
plt.errorbar(x_line, y_data, yerr = y_error  , lw=line_width, capsize=0 ,c=data_color,ls=data_line,marker=data_marker,ms=data_point_size , alpha=line_alpha )

#############################################################################################
# handle the legend
#############################################################################################

legend_data,     = plt.plot( -x_line,-x_line, lw=line_width, c=data_color,ls='-',marker=data_marker,ms=data_point_size , alpha=line_alpha , label=r'$\rm{Data}$')
legend_theory_A, = plt.plot( -x_line,-x_line, lw=line_width, c=data_color,ls='-' , alpha=line_alpha , label=r'$\rm{Theory \, A}$')
legend_theory_B, = plt.plot( -x_line,-x_line, lw=line_width, c=data_color,ls='--', alpha=line_alpha , label=r'$\rm{Theory \, B}$')
legend_fill,     = plt.plot( -x_line,-x_line, lw=9, c=color_indigo,ls='-' , alpha=fill_alpha , label=r'$\rm{Theory \, Range}$')
plt.legend(handles=[  legend_theory_A , legend_theory_B ,  legend_data, legend_fill ], ncol=2, numpoints =1 , loc=2, fontsize=font_size_ticks)

# final plot settings
plt.subplots_adjust( hspace=0.05, wspace=0.05)
plt.tight_layout() # matplotlib usually wastes lots of space - this reduces the wasted space

#############################################################################################
# save the figure
#############################################################################################

figure_path = 'boiler_figures'
figure_tag = 'generated_data_plot'
figure_suffix = '.pdf'
figure_name = figure_path + '/' + figure_tag + figure_suffix

if os.path.isdir( figure_path ):
    print 'Figure path ok'
else:
    os.mkdir( figure_path )

plt.savefig( figure_name )
