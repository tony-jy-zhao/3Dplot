from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import numpy as np

x_list = [-1, 2, 10, 3]
y_list = [3, -3, 4, 7]
z_list = [5, 1, 2.5, 4.5]

# f will be a function with two arguments (x and y coordinates),
# but those can be array_like structures too, in which case the
# result will be a matrix representing the values in the grid
# specified by those arguments
f = interp2d(x_list, y_list, z_list, kind="linear")

x_coords = np.arange(min(x_list), max(x_list) + 1)
y_coords = np.arange(min(y_list), max(y_list) + 1)
Z = f(x_coords, y_coords)

fig = plt.imshow(Z,
                 extent=[min(x_list), max(x_list), min(y_list), max(y_list)],
                 origin="lower")

# Show the positions of the sample points, just to have some reference
fig.axes.set_autoscale_on(False)
plt.scatter(x_list, y_list, 400, facecolors='none')
plt.show()