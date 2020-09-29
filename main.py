from catmull_rom_spline import catmull_rom, normalize, plot_rad
from scipy.interpolate import splev, splprep, interp1d, interp2d
import numpy as np
import json
import io
import os

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    res = 5

    for path in range(20):
        jsonPath = os.path.join('wp10', str(path) + '.json')
        with open(jsonPath, 'r') as jsonfile:
            data = np.array(json.load(jsonfile))

        p_x = data[:, 0]
        p_y = data[:, 1]
        p_t = np.arange(len(p_x))

        # catmull-rom
        # s_x, s_y = catmull_rom(p_x, p_y, res)

        # BSpline
        # tck, u = splprep([p_x, p_y], k=3)
        # u = np.linspace(0, 1, 50)
        # s_x, s_y = np.array(splev(u, tck))

        # bilinear interpolate
        # f = interp1d(p_x, p_y)
        # s_x = np.linspace(0, 4, 50)
        # s_y = f(s_x)

        # bicubic interepolate
        # f = interp2d(p_t, p_x, p_y, kind='cubic')
        # s_t = np.linspace(0, len(p_t), 50)


        # fancy plotting
        fig, ax = plt.subplots(2, 2)

        ax[0, 1].set_aspect('equal', 'box')
        ax[0, 1].scatter(s_x, s_y, s=1)
        ax[0, 1].scatter(p_x, p_y, s=1)

        s_rad = plot_rad(s_x, s_y) 
        ax[1, 1].plot(s_rad)

        ax[0, 0].set_aspect('equal', 'box')
        ax[0, 0].scatter(p_x, p_y, s=1)

        p_rad = plot_rad(p_x, p_y) 
        ax[1, 0].plot(p_rad)

        plt.show()