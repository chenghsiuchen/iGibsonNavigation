#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
import json
import io
import os

def catmull_rom_one_point(x, v0, v1, v2, v3):
    """Computes interpolated y-coord for given x-coord using Catmull-Rom.

    Computes an interpolated y-coordinate for the given x-coordinate between
    the support points v1 and v2. The neighboring support points v0 and v3 are
    used by Catmull-Rom to ensure a smooth transition between the spline
    segments.
    Args:
        x: the x-coord, for which the y-coord is needed
        v0: 1st support point
        v1: 2nd support point
        v2: 3rd support point
        v3: 4th support point
    """
    c1 = 1. * v1
    c2 = -.5 * v0 + .5 * v2
    c3 = 1. * v0 + -2.5 * v1 + 2. * v2 -.5 * v3
    c4 = -.5 * v0 + 1.5 * v1 + -1.5 * v2 + .5 * v3
    return (((c4 * x + c3) * x + c2) * x + c1)

def catmull_rom(p_x, p_y, res):
    """Computes Catmull-Rom Spline for given support points and resolution.

    Args:
        p_x: array of x-coords
        p_y: array of y-coords
        res: resolution of a segment (including the start point, but not the
            endpoint of the segment)
    """
    # create arrays for spline points
    x_intpol = np.empty(res*(len(p_x)-1) + 1)
    y_intpol = np.empty(res*(len(p_x)-1) + 1)

    # set the last x- and y-coord, the others will be set in the loop
    x_intpol[-1] = p_x[-1]
    y_intpol[-1] = p_y[-1]

    # loop over segments (we have n-1 segments for n points)
    for i in range(len(p_x)-1):
        # set x-coords
        x_intpol[i*res:(i+1)*res] = np.linspace(
            p_x[i], p_x[i+1], res, endpoint=False)
        if i == 0:
            # need to estimate an additional support point before the first
            y_intpol[:res] = np.array([
                catmull_rom_one_point(
                    x,
                    p_y[0] - (p_y[1] - p_y[0]), # estimated start point,
                    p_y[0],
                    p_y[1],
                    p_y[2])
                for x in np.linspace(0.,1.,res, endpoint=False)])
        elif i == len(p_x) - 2:
            # need to estimate an additional support point after the last
            y_intpol[i*res:-1] = np.array([
                catmull_rom_one_point(
                    x,
                    p_y[i-1],
                    p_y[i],
                    p_y[i+1],
                    p_y[i+1] + (p_y[i+1] - p_y[i]) # estimated end point
                ) for x in np.linspace(0.,1.,res, endpoint=False)])
        else:
            y_intpol[i*res:(i+1)*res] = np.array([
                catmull_rom_one_point(
                    x,
                    p_y[i-1],
                    p_y[i],
                    p_y[i+1],
                    p_y[i+2]) for x in np.linspace(0.,1.,res, endpoint=False)])


    return (x_intpol, y_intpol)

def update(frame, ax, x, y):
    # p.set_offsets(np.array([x[frame], y[frame]]))
    aspect = (y[frame + 1] - y[frame]) / (x[frame + 1] - x[frame])
    dx = x[frame + 1] - x[frame]
    dy = dx * aspect
    # print(dx, dy)
    p = plt.arrow(x[frame], y[frame], dx, dy, width=0.02)
    ax.add_patch(p)
    return p,

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    # set the resolution (number of interpolated points between each pair of
    # points, including the start point, but excluding the endpoint of each
    # interval)
    res = 50

    # generate some random support points
    # p_x = np.arange(-10,11, dtype='float32')
    # p_y = np.zeros_like(p_x)
    # for i in range(len(p_x)):
    #     p_y[i] = np.random.rand() * 20. - 10.

    jsonPath = os.path.join('wp10', '0.json')
    with open(jsonPath, 'r') as jsonfile:
        data = np.array(json.load(jsonfile))

    p_x = data[:, 0]
    p_y = data[:, 1]

    # do the catmull-rom
    s_x, s_y = catmull_rom(p_x, p_y, res)

    # fancy plotting
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')

    plt.plot(s_x, s_y)
    # plt.scatter(s_x, s_y, s=1)

    FuncAnimation(fig, update, frames=(len(s_x) - 1), fargs=(ax, s_x, s_y), interval=20, blit=True)
    
    plt.show()

# vim: set ts=4 sw=4 sts=4 expandtab:
