# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 17:41:04 2023

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
    step_20um_index = 20/steps
    
    if int(x_plot_index-step_20um_index) <0:
        continue
    
    x = x1[int(x_plot_index-step_20um_index):int(x_plot_index+step_20um_index)]
    df1 = df[:,int(x_plot_index-step_20um_index):int(x_plot_index+step_20um_index)]
    
    
    print(z[i])
    
    colorbarmax = df1.max().max()
    
    X,Y = np.meshgrid(x,y)
    fig, ax = plt.subplots(figsize=(5, 4), tight_layout=True)

    ax.contourf(X,Y,df1, 200, cmap='viridis')
    ax.set_aspect('equal')  # Set the aspect ratio to 'equal'
    
    
    # Remove x and y axes and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Remove any labels or titles
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('')
    
    plt.margins(0,0)
    plt.title(str(z[i])+'\n\n\n\n', fontweight="bold")
    plt.show()
    plt.close()
