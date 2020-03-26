from math import *
import numpy as np


def spherical(x, y, z):
    r = sqrt(abs(x ** 2 + y ** 2 + z ** 2))  # x,y,z are the initial values(middle)
    phi = np.arccos(z / r) * 180 / pi
    theta = atan2(y, x) * 180 / pi
    if theta < 0:
        theta = 360 + theta
    print("The radius is", r, "meter")
    print("The angle phi is", phi, "degrees")
    print("The angle theta is", theta, "degrees")
    return r, phi, theta


def latlongheight(x, y, z):
    r = sqrt(abs(x ** 2 + y ** 2 + z ** 2))  # x,y,z are the initial values
    phi = np.arctan(z / sqrt(x ** 2 + y ** 2)) * 180 / pi
    # theta = np.arctan(y/x)*180/pi
    theta = atan2(y, x) * 180 / pi
    Height = r - 6378137  # Height above or below sea level
    if theta < 0:
        theta = 360 + theta
    print("The height is", Height, "meter")
    print("The latitude is", phi, "degrees N")
    print("The longitude is", theta, "degrees E")
    return Height, phi, theta


def rotation(x, y, z, x1, y1, z1, x2, y2, z2):  # x1, y1 and z1 are the current values(standard deviation)
    # x,y,z are the initial values(middle coordinates)
    r = sqrt(abs(
        x ** 2 + y ** 2 + z ** 2))  # x2, y2, z2 are the initial values(middle standard deviations)
    phi = np.arctan(z / sqrt(x ** 2 + y ** 2))
    theta = atan2(y, x)
    # if theta <0:
    #   theta = 2*pi + theta
    G = np.array([[-sin(theta), cos(theta), 0],
                  [-sin(phi) * cos(theta), -sin(phi) * sin(theta), cos(phi)],
                  [cos(phi) * cos(theta), cos(phi) * sin(theta), sin(phi)]])

    D = G[0, 0] * abs(x1 - x2) + G[0, 1] * abs(y1 - y2) + G[0, 2] * abs(z1 - z2)  # East
    E = G[1, 0] * abs(x1 - x2) + G[1, 1] * abs(y1 - y2) + G[1, 2] * abs(z1 - z2)  # North
    F = G[2, 0] * abs(x1 - x2) + G[2, 1] * abs(y1 - y2) + G[2, 2] * abs(z1 - z2)  # Up

    print("East is", D, "meters")
    print("North is", E, "meters")
    print("Up is", F, "meters")
    return D, E, F