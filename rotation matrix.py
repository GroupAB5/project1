"""script will go from ecef(xyz) to enu
for both the coordinates as the covariance matrix.
25dec 2004 will be set as zero for now"""


import numpy as np
from math import *
from scipy import optimize
import matplotlib.pyplot as plt

a = 6378137.0                 #  WGS 84 earth radius at equator in [m] see link p.[3-5,3-7]
b = 6356752.3142
e_2 = 6.69437999014*10**3     # ecentricity squared [https://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf]

def ecef_to_geodetic(x,y,z):
    """Bases on http://clynchg3c.com/Technote/geodesy/coordcvt.pdf
    warning!! in radians so not actual longitude lattitude as this would be in deg"""
    a = 6378137.0  # WGS 84 earth radius at equator in [m] see link p.[3-5,3-7]
    b = 6356752.3142
    e_2 = 6.69437999014 * 10 ** 3  # ecentricity squared [https://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf]

    longitude = np.arctan2(y,x)
    p = np.sqrt(x**2 + y**2)

    # using the LiN AND WANG'S Method http://www.mygeodesy.id.au/documents/Transforming%20Cartesian%20Coordinates.pdf
    m0 = (a*b*(a**2 *z**2 + b**2 * p**2)**(3/2) - a**2 * b**2 *(a**2 * z**2 + b**2 * p**2))/(2*(a**4 *z**2 + b**4 * p**2))
    print("m0 = ",m0)

    def f(m): return(((p**2)/(a+(2*m/a))**2) + ((z**2)/(b+(2*m)/b)**2) - 1)
    def dfdm(m): return(-4*(((p**2)/(a*(a+(2*m/a))**3)) + ((z**2)/(b*(b+(2*m)/b)**3))))
    m = optimize.newton(f,m0,dfdm, maxiter = 1000)
    print("mend = ", m)


    PE = p/(1 + (2*m)/a**2)
    ZE = z/(1 + (2*m)/b**2)
    phi = np.arctan2((ZE * a**2),(PE * b**2))
    if p+abs(z) < PE +abs(ZE):
        h = -np.sqrt((p-PE)**2 + (z+ZE)**2)
    else:
        h = np.sqrt((p-PE)**2 + (z+ZE)**2)


    lattitude = phi
    height = h

    return(lattitude,longitude,height)

def rotation(lat0,lon0):
    """lat0 and lon0 should be the reference geodetic longitude and lattitude in radians
    these can be obtained by using ecef_to_geodetic with reference x,y,z"""
    phi = lon0
    lamb = lat0
    G = np.array([[-sin(lamb), cos(lamb), 0],
                  [-sin(phi) * cos(lamb), -sin(phi) * sin(lamb), cos(phi)],
                  [cos(phi) * cos(lamb), cos(phi) * sin(lamb), sin(phi)]])
    return (G)

def ecef_to_enu(x,y,z,G,xr,yr,zr):
    enu = G*np.array([[x-xr],
                      [y-yr],
                      [z-zr]])
    return(enu)

def ecefcov_to_enucov(ecefcov,G):
    """law of propagation of variance (ony valid if ecef and enu are linear related and enu = A*xyz +b
    y = Ax +"""
    enucov = G*ecefcov*np.transpose(G)
    return(ecefcov)





Covar = np.array([[ 4.07266986e-07, -3.05867274e-07,  2.84446569e-07],
       [-3.05867274e-07,  1.74258119e-06, -1.39395932e-06],
       [ 2.84446569e-07, -1.39395932e-06,  1.77034639e-06]])

#ALO 25december 2004
x0 = 0.918129379046376*10**6
y0 = -0.434607125236106*10**7
z0 = 0.456197785308569*10**7

#ALO 31 december ... (last date availible)
x  = 0.918129252507942*10**6
y  = -0.434607129935392*10**7
z  = 0.456197789366776*10**7

lst = ecef_to_geodetic(x0,y0,z0)
lat0,lon0 = lst[0],lst[1]

G = rotation(lat0,lon0)
enu = ecef_to_enu(x,y,z,G,x0,y0,z0)
print("enu",enu)
newCovar = ecefcov_to_enucov(Covar,G)
print(newCovar)
print(np.sqrt(newCovar))
