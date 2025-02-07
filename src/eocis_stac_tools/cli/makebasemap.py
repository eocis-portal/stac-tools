import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as feature

plt.figure(figsize=(8, 4))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_xmargin(0)
ax.set_ymargin(0)
ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())

ax.add_feature(feature.LAND)
ax.add_feature(feature.OCEAN)
ax.add_feature(feature.COASTLINE, linewidth=1)


plt.savefig("test.png")