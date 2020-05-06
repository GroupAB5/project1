"""script will go from ecef(xyz) to enu
"""


import numpy as np
from math import *
from scipy import optimize
import matplotlib.pyplot as plt

a = 6378137.0                 #  WGS 84 earth radius at equator in [m] see link p.[3-5,3-7]
b = 6356752.3142
e_2 = 6.69437999014*10**3     # ecentricity squared [https://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf]

def ecef_to_geodetic(x,y,z):
    """Bases on http://clynchg3c.com/Technote/geodesy/coordcvt.pdf
    warning!! 1. this i geodetic longitude and lattitude thus not suitable to setup rotation matrix 2. these are in radians"""
    a = 6378137.0  # WGS 84 earth radius at equator in [m] see link p.[3-5,3-7]
    b = 6356752.3142
    e_2 = 6.69437999014 * 10 ** 3  # ecentricity squared [https://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf]

    longitude = np.arctan2(y,x)
    p = np.sqrt(x**2 + y**2)

    # using the LiN AND WANG'S Method http://www.mygeodesy.id.au/documents/Transforming%20Cartesian%20Coordinates.pdf

    #newton method
    m0 = (a*b*(a**2 *z**2 + b**2 * p**2)**(3/2) - a**2 * b**2 *(a**2 * z**2 + b**2 * p**2))/(2*(a**4 *z**2 + b**4 * p**2))
    def f(m): return(((p**2)/(a+(2*m/a))**2) + ((z**2)/(b+(2*m)/b)**2) - 1)
    def dfdm(m): return(-4*(((p**2)/(a*(a+(2*m/a))**3)) + ((z**2)/(b*(b+(2*m)/b)**3))))
    m = optimize.newton(f,m0,dfdm, maxiter = 1000000)

    PE = p/(1 + (2*m)/a**2)
    ZE = z/(1 + (2*m)/b**2)
    phi = np.arctan2((ZE * a**2),(PE * b**2))
    h = np.sqrt((PE-p)**2+(ZE-z)**2)
    lattitude = phi
    height = h

    return(lattitude,longitude,height)



def rotation(x,y,z):
    """lat0 and lon0 should be the reference geodetic longitude and lattitude in radians
    these can be obtained by using ecef_to_geodetic with reference x,y,z"""
    phi = np.arctan(z/sqrt(x**2+y**2))
    lamb = np.arctan2(y,x)
    G = np.array([[-sin(lamb), cos(lamb), 0],
                  [-sin(phi) * cos(lamb), -sin(phi) * sin(lamb), cos(phi)],
                  [cos(phi) * cos(lamb), cos(phi) * sin(lamb), sin(phi)]])
    return (G)



#Covar = np.array([[ 4.07266986e-07, -3.05867274e-07,  2.84446569e-07],
      # [-3.05867274e-07,  1.74258119e-06, -1.39395932e-06],
       #[ 2.84446569e-07, -1.39395932e-06,  1.77034639e-06]])
Cov_xyz = np.array([[(0.638174730064971*(10**-3))**2, -0.363075461356061*0.638174730064971*(10**-3)*0.132006863142369*(10**-2), 0.334990099434831*0.638174730064971*(10**-3)*0.133054364430706*(10**-2)],
                  [-0.363075461356061*0.638174730064971*(10**-3)*0.132006863142369*(10**-2), (0.132006863142369*(10**-2))**2, -0.793641672660415*0.132006863142369*(10**-2)*0.133054364430706*(10**-2)],
                  [0.334990099434831*0.638174730064971*(10**-3)*0.133054364430706*(10**-2), -0.793641672660415*0.132006863142369*(10**-2)*0.133054364430706*(10**-2), (0.133054364430706*(10**-2))**2]])


#ALO 31 december ... (last date availible)
x  = 0.918129252507942*10**6
y  = -0.434607129935392*10**7
z  = 0.456197789366776*10**7


lst = ecef_to_geodetic(x,y,z)
lat0,lon0,height = lst[0],lst[1],lst[2]

G = rotation(x,y,z)
print(G)
Cov_ENU = G.dot(Cov_xyz).dot(np.transpose(G))


F4 = np.sqrt(Cov_ENU[0, 0]) * 1000
F5 = np.sqrt(Cov_ENU[1, 1]) * 1000
F6 = np.sqrt(Cov_ENU[2, 2]) * 1000

print(180*lat0/pi,180*lon0/pi,height)
print(F4,F5,F6)
