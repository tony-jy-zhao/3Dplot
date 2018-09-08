import filePatch
import pandas as pd
import filePatch
import numpy as np
import matplotlib.pylab as plt
import scipy
from scipy.interpolate import interp2d
from mpl_toolkits.mplot3d import Axes3D


class Draw_2d:
    def __init__(self):
        self.data = pd.DataFrame()

    def get_dataframe(self, dir_path):
        sa = filePatch.Signals_all()
        self.data = self.data.append(sa.add_all(dir_path))

    def draw3d(self):
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        plt.style.use('seaborn-white')
        ax = plt.figure().gca(projection='3d')
        skip_every = 5
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][::skip_every]
        ax.scatter(xs, ys, zs)
        ax.plot(xs, ys, zs)
        ax.set_xlabel('Collision Energy')
        ax.set_ylabel('Q2RF')
        ax.set_zlabel('Signal Intensity')
        plt.show()

    def draw2dheatmap(self):
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        skip_every = 5
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][
                                                                                         ::skip_every]
        f = interp2d(xs, ys, zs, kind="linear")

        x_coords = np.arange(min(xs), max(xs) + 1)
        y_coords = np.arange(min(ys), max(ys) + 1)
        Z = f(x_coords, y_coords)

        fig = plt.imshow(Z,
                         extent=[min(xs), max(xs), min(ys), max(ys)],
                         origin="lower", aspect='auto')

        fig.axes.set_autoscale_on(False)
        plt.scatter(xs, ys, 400, facecolors='none')

        plt.xlabel('Collision Energy')
        plt.ylabel('Q2RF')
        plt.show()

    def draw2d_scipy(self):
        '''
        The best plot solution.
        Interestingly a simple: plt.scatter(xs, ys, c=zs) works as well.
        :return:
        '''
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        skip_every = 5
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][
                                                                                         ::skip_every]

        plt.scatter(xs, ys, c=zs)
        # Set up a regular grid of interpolation points
        xi, yi = np.linspace(min(xs), max(xs), 100), np.linspace(min(ys), max(ys), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate
        rbf = scipy.interpolate.Rbf(xs, ys, zs, function='linear')
        zi = rbf(xi, yi)

        plt.imshow(zi, vmin=min(zs), vmax=max(zs), origin='lower',
                   extent=[min(xs), max(xs), min(ys), max(ys)], aspect='auto')
        #plt.scatter(xs, ys, c=zs)
        plt.colorbar()
        plt.show()

    

if __name__ == '__main__':
    draw_2d = Draw_2d()
    draw_2d.get_dataframe('468-121_n')
    #draw_2d.draw2dheatmap()
    #draw_2d.draw3d()
    draw_2d.draw2d_scipy()