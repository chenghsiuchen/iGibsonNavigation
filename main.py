from catmull_rom_spline import catmull_rom, normalize, plot_rad
from scipy.interpolate import splev, splprep, interp1d, interp2d
import numpy as np
import json
import math
import io
import os

def offset(x):
    return np.append(x[0] - x[1] + x[0], x)

def lerp(x, y, rad):
    insert_cnt = 0
    for i in range(len(rad) - 1):
        diff = abs(rad[i] - rad[i + 1])
        # print(i, rad[i], rad[i+1], diff)
        if diff > 0.3:
            div = math.ceil(diff / 0.1)
            _i = i + insert_cnt
            r_x = [x[_i - 1] + (x[_i] - x[_i - 1]) / div * (j + 1) for j in range(div - 1)]
            r_y = [y[_i - 1] + (y[_i] - y[_i - 1]) / div * (j + 1) for j in range(div - 1)]
            print(x[_i - 1], r_x, x[_i])
            print(y[_i - 1], r_y, y[_i])
            x = np.concatenate((x[:_i + 1], np.array(r_x), x[_i + 1:]))
            y = np.concatenate((y[:_i + 1], np.array(r_y), y[_i + 1:]))
            insert_cnt += len(r_x)

    return x, y



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    res = 5

    for path in range(1):
        jsonPath = os.path.join('wp10', str(path) + '.json')
        with open(jsonPath, 'r') as jsonfile:
            data = np.array(json.load(jsonfile))

        p_x = data[:, 0]
        p_y = data[:, 1]
        p_t = np.arange(len(p_x))
        p_rad = plot_rad(offset(p_x), offset(p_y))

        s_x, s_y = lerp(p_x, p_y, p_rad)

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

        s_rad = plot_rad(offset(s_x), offset(s_y))

        # fancy plotting
        fig, ax = plt.subplots(2, 2)

        ax[0, 1].set_aspect('equal', 'box')
        ax[0, 1].scatter(s_x, s_y, s=1)
        ax[0, 1].scatter(p_x, p_y, s=1)
         
        ax[1, 1].plot(s_rad)
        ax[1, 1].scatter(range(len(s_rad)), s_rad, s=5)

        ax[0, 0].set_aspect('equal', 'box')
        ax[0, 0].scatter(p_x, p_y, s=1)

        ax[1, 0].plot(p_rad)
        ax[1, 0].scatter(range(len(p_rad)), p_rad, s=5)

        plt.show()