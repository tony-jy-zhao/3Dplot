# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:20:17 2018

@author: tony.zhao2
"""

# libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kde

# create data
x = np.random.normal(size=500)
y = x * 3 + np.random.normal(size=500)

# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
nbins = 300
k = kde.gaussian_kde([x, y])
xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

# Make the plot
plt.pcolormesh(xi, yi, zi.reshape(xi.shape))
plt.show()

# Change color palette
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.Greens_r)
plt.show()
