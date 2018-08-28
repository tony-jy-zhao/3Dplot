import filePatch
import pandas as pd
import filePatch
import numpy as np
import matplotlib.pylab as plt
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
        skip_every = 50
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][::skip_every]
        ax.scatter(xs, ys, zs)
        ax.plot(xs, ys, zs)
        ax.set_xlabel('Collision Energy')
        ax.set_ylabel('Q2RF')
        ax.set_zlabel('Signal Intensity')
        plt.show()

    def draw2dheat(self):
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        plt.style.use('seaborn-white')
        skip_every = 10
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][
                                                                                         ::skip_every]
        # https://stackoverflow.com/questions/26635870/plot-x-y-z-triples-on-2d-plane-with-a-colormap
        xx, yy = np.meshgrid[0:max(ys):800j, 0:max(xs):800j]
        # zz =
        plt.imshow()
        plt.xlabel('Collision Energy')
        plt.ylabel('Q2RF')
        plt.show()

    def draw3d_mayavi(self):
        '''
        Half way down. Guess because parts of data missing
        :return:
        '''
        from mayavi import mlab
        data = self.data
        pts = list(map(lambda x, y: x + tuple([y]), data.index.values.tolist(), np.squeeze(data.values)))
        plt.style.use('seaborn-white')
        ax = plt.figure().gca(projection='3d')
        skip_every = 10
        xs, ys, zs = list(zip(*pts))[0][::skip_every], list(zip(*pts))[1][::skip_every], list(zip(*pts))[2][
                                                                                         ::skip_every]

        pts = mlab.points3d(xs, ys, zs, zs)
        mesh = mlab.pipeline.delaunay2d(pts)
        pts.remove()

        surf = mlab.pipeline.surface(mesh)

        mlab.xlabel('Collision Energy')
        mlab.ylabel('Q2RF')
        mlab.show()


if __name__ == '__main__':
    draw_2d = Draw_2d()
    draw_2d.get_dataframe('322-60')
    draw_2d.draw3d()
