from catmull_rom_spline import catmull_rom, normalize, plot_rad, plot_drad
from CatmullRomSpline import CatmullRomChain
from scipy.interpolate import splev, splprep, CubicSpline
from scipy.integrate import odeint
import numpy as np
import json
import math
import io
import os
from geomdl import BSpline, fitting

def offset(x):
    return np.append(x[0] - x[1] + x[0], x)

def offset_xy(xy):
    return np.concatenate((np.array([xy[0] - xy[1] + xy[0] - [0.1, 0]]), xy, np.array([xy[-1] + xy[-2] - xy[-1]])))

def clothoid_ode_rhs(state, s, kappa0, kappa1):
    x, y, theta = state[0], state[1], state[2]
    return np.array([np.cos(theta), np.sin(theta), kappa0 + kappa1*s])
def eval_clothoid(x0,y0,theta0, kappa0, kappa1, s):
    return odeint(clothoid_ode_rhs, np.array([x0,y0,theta0]), s, (kappa0, kappa1))

def smooth_filter(p_x, p_y):
    size = 2 # filter range
    
    x = []
    y = []
    for i in range(size):
        x.append(p_x[i])
        y.append(p_y[i])

    for i in range(size, len(p_x) - size, 1):
        new_x = 0
        new_y = 0
        for j in range(size * 2 + 1):
            idx = j - size
            new_x += p_x[i + idx]
            new_y += p_y[i + idx]

        new_x /= (size * 2 + 1)
        new_y /= (size * 2 + 1)

        x.append(new_x)
        y.append(new_y)

    for i in range(size):
        idx = i - size
        x.append(p_x[idx])
        y.append(p_y[idx])
    return np.array(x), np.array(y)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    res = 50

    for path in range(20):
        jsonPath = os.path.join('wp10', str(path) + '.json')
        with open(jsonPath, 'r') as jsonfile:
            data = np.array(json.load(jsonfile))

        p_x = data[:, 0]
        p_y = data[:, 1]
        p_t = np.arange(len(p_x))
        p_rad = plot_rad(offset(p_x), offset(p_y))

        # s_x, s_y = lerp(p_x, p_y, p_rad)

        # catmull-rom
        # s_x, s_y = catmull_rom(p_x, p_y, res)

        # centripetal catmull-rom
        # p = offset_xy(data)
        # c = CatmullRomChain(p)
        # s_x, s_y = zip(*c)

        # BSpline
        _p_x, _p_y = smooth_filter(p_x, p_y)
        tck_x, u_x = splprep([p_t, p_x], k=3)
        tck_y, u_y = splprep([p_t, p_y], k=3)
        u = np.linspace(0, 1, 50)
        _, s_x = np.array(splev(u, tck_x))
        _, s_y = np.array(splev(u, tck_y))

        # cubic spline
        # _p_x, _p_y = smooth_filter(p_x, p_y)
        # cs_x = CubicSpline(p_t, _p_x)
        # cs_y = CubicSpline(p_t, _p_y)
        # u = np.linspace(0, p_t[-1], 500)
        # s_x = cs_x(u)
        # s_y = cs_y(u)

        # NURBS
        # crv = fitting.interpolate_curve(data.tolist(), 3)
        # u = np.linspace(0, 1, 500)
        # pts = np.array(crv.evaluate_list(u))
        # s_x = pts[:, 0]
        # s_y = pts[:, 1]

        # clothoid


        s_rad = plot_rad(offset(s_x), offset(s_y))
        s_drad = plot_drad(s_rad)

        # fancy plotting
        fig, ax = plt.subplots(2, 2)

        ax[0, 0].set_aspect('equal', 'box')
        ax[0, 0].invert_xaxis()
        ax[0, 0].invert_yaxis()
        ax[0, 0].scatter(s_x, s_y, s=1)
        ax[0, 0].scatter(p_x, p_y, s=1)
        ax[0, 0].scatter(_p_x, _p_y, s=1)

        ax[0, 1].scatter(range(len(s_drad)), s_drad, s=1)
         
        # ax[1, 1].plot(s_rad)
        ax[1, 1].scatter(range(len(s_rad)), s_rad, s=1)

        # ax[1, 0].plot(p_rad)
        ax[1, 0].scatter(range(len(p_rad)), p_rad, s=1)

        # fig = plt.figure()
        # ax = fig.gca(projection='3d')
        # ax.plot3D(s_x, s_y, range(len(s_x)))

        plt.show()