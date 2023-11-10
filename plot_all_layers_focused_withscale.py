# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:54:39 2023

@author: limyu
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:14:01 2023

@author: limyu
"""


import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from sklearn.metrics import mean_squared_error
from scipy import interpolate
from scipy.signal import chirp, find_peaks, peak_widths
from scipy.stats import linregress
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import time

file_list = "grating12pitch100", "grating12_11pitch6_4", "grating012umpitch05dutycycle60um"

file = "grating012umpitch05dutycycle50um"
# Load the h5 file
with h5py.File("C:\\Users\\limyu\\Google Drive\\3d plots\\"+file+".h5", 'r') as f:
    # Get the dataset
    dset = f[file]
    # Load the dataset into a numpy array
    arr_3d_loaded = dset[()]

z_cutoff = 0
I = np.arange(z_cutoff,317,1)
print(I)


for i in I:
    
    x1 = np.linspace(-20, 80, num=arr_3d_loaded.shape[0])
    y = np.linspace(-25, 25, num =arr_3d_loaded.shape[1])
    z = np.linspace(-5, 45, num =arr_3d_loaded.shape[2]-z_cutoff)
    
    z_plane_df = arr_3d_loaded[:,:,i]
    df = z_plane_df.transpose()
    x_plot = df[int(df.shape[0]/2), :]
    x_plot_index = int(np.where(x_plot == max(x_plot))[0])
    
    x_max = x1[x_plot_index]
    steps = 100/arr_3d_loaded.shape[0]
    step_20um_index = 15/steps
    
    if int(x_plot_index-step_20um_index) <0:
        continue
    
    x = x1[int(x_plot_index-step_20um_index):int(x_plot_index+step_20um_index)]
    df1 = df[:,int(x_plot_index-step_20um_index):int(x_plot_index+step_20um_index)]
    
    
    print(z[i])
    
    colorbarmax = df1.max().max()
    
    X,Y = np.meshgrid(x,y)
    fig = plt.figure(figsize=(5, 4))
    ax = plt.axes()
    cp=ax.contourf(X,Y,df1, 200, zdir='z', offset=-100, cmap='viridis')
    clb=fig.colorbar(cp, ticks=(np.around(np.linspace(0.0, colorbarmax, num=6), decimals=3)).tolist())
    clb.ax.set_title('Electric Field (eV)', fontweight="bold")
    for l in clb.ax.yaxis.get_ticklabels():
        l.set_weight("bold")
        l.set_fontsize(15)
    ax.set_xlabel('x-position (µm)', fontsize=20, fontweight="bold", labelpad=1)
    ax.set_ylabel('y-position (µm)', fontsize=20, fontweight="bold", labelpad=1)
    ax.xaxis.label.set_fontsize(20)
    ax.xaxis.label.set_weight("bold")
    ax.yaxis.label.set_fontsize(20)
    ax.yaxis.label.set_weight("bold")
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_yticklabels(ax.get_yticks(), weight='bold')
    ax.set_xticklabels(ax.get_xticks(), weight='bold')
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.title(str(z[i])+'\n\n\n\n', fontweight="bold")
    plt.show()
    plt.close()
