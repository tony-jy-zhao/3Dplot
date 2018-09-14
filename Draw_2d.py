import filePatch
import pandas as pd
import filePatch
import numpy as np
import matplotlib.pylab as plt
import scipy
from scipy.interpolate import interp2d
import ParseData
from mpl_toolkits.mplot3d import Axes3D


class Draw_2d:

    def __init__(self, sf=True):
        self.data = pd.DataFrame()
        ParseData.smooth_flag = sf
        self.dir = ""

    def get_dataframe(self, dir_path):
        self.dir = dir_path
        sa = filePatch.Signals_all()
        self.data = self.data.append(sa.add_all(dir_path))

    def create_title(self):
        import re
        num = re.findall('\d+', self.dir)
        self.dir = num[-2] + "-" + num[-1]
        return "trans from mz=" + num[-2] + " to " + num[-1]

    def draw3d(self):
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        plt.style.use('seaborn-white')
        ax = plt.figure().gca(projection='3d')
        skip_every = 5
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][
                                                                                         ::skip_every]
        ax.scatter(xs, ys, zs)
        ax.plot(xs, ys, zs)
        ax.set_xlabel('Collision Energy')
        ax.set_ylabel('Q2RF')
        ax.set_zlabel('Signal Intensity')
        plt.show()

    def draw2dheatmap(self):
        '''
        Because of the bad interp2d func, this plot is very off
        :return:
        '''

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

    def draw2d_scipy(self, s='n'):
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
        plt.figure(figsize=(4, 3))
        if s == 's':
            plt.scatter(xs, ys, c=zs)
        elif s == 'n':
            # Set up a regular grid of interpolation points
            xi, yi = np.linspace(min(xs), max(xs), 100), np.linspace(min(ys), max(ys), 100)
            xi, yi = np.meshgrid(xi, yi)

            # Interpolate
            rbf = scipy.interpolate.Rbf(xs, ys, zs, function='linear')
            zi = rbf(xi, yi)

            plt.imshow(zi, vmin=min(zs), vmax=max(zs), origin='lower',
                       extent=[min(xs), max(xs), min(ys), max(ys)], aspect='auto')
            # plt.scatter(xs, ys, c=zs)

        plt.xlabel('Collision Energy')
        plt.ylabel('Q2RF')
        plt.title(self.create_title())
        plt.colorbar()
        plt.savefig(self.dir + '.png', bbox_inches='tight', dpi=300)
        plt.show()


class Create_All_Figs:
    def __init__(self):
        self.dir_list = []

    def Create_All_Figs(self):
        return


if __name__ == '__main__':
    '''
    The selection between raw data or smoothed data occurs in ParseData.py .first() or .last()
    '''
    draw_2d = Draw_2d(sf=True)
    draw_2d.get_dataframe('417-121')
    # draw_2d.draw2dheatmap()
    # draw_2d.draw3d()
    draw_2d.draw2d_scipy('n')
