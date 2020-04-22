import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from ConversionXYZ2NEU import latlongheight
import rewriteFiles as rf
#import coordinate_transformation as ct


coordinates, stations, date = rf.getCoord("C:/Users/adask/Desktop/TUDelft/Test, analysis and simulation/data/gps_data/PZITRF08001.00X") # first coordinate file wim ever sent (use as test)
stat_x = coordinates[:, 0]
stat_y = coordinates[:, 1]
stat_z = coordinates[:, 2]

coord_transformed = [list(latlongheight(stat_x[i], stat_y[i], stat_z[i])) for i in range(len(stat_x))]
map_data = np.array(coord_transformed)

lat = map_data[:, 1] # latitude
lon = map_data[:, 2] # longitude

# ------- note everything from here on may be changed to make it work, I wrote this code without being able to run it as i had trouble installing Basemap ------
# plotting on map
m = Basemap(width=12000000,height=9000000,projection='moll',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
# draw a boundary around the map, fill the background.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
# label parallels on right and top
# meridians on bottom and left
parallels = np.arange(-90.,91,30.)
meridians = np.arange(10.,351.,20.) # maybe should be changed to [-180,180]

# convert to map coordinates
xpt,ypt = m(lon,lat)

# plot and show
m.plot(xpt, ypt, 'ro')
plt.show()
