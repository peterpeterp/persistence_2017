import os,sys,glob,time,collections,gc,pickle
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pylab as plt 

from matplotlib import rc
rc('text', usetex=True)

os.chdir('/Users/peterpfleiderer/Documents/Scripts/allgemeine_scripte')
try:
    import plot_map as plot_map; reload(plot_map)
except ImportError:
    raise ImportError(
        "cannot find plot_map code")
from plot_map import col_conv
os.chdir('/Users/peterpfleiderer/Documents/Projects/HAPPI_persistence')

persis = plot_map.make_colormap([col_conv('blue'), col_conv('green'), 0.33, col_conv('green'), col_conv('yellow'), 0.66, col_conv('yellow'), col_conv('red')])


# pkl_file = open('data/Plus15-Future_summary.pkl', 'rb')
# Fu15_dict = pickle.load(pkl_file)	;	pkl_file.close()  

# pkl_file = open('data/Plus20-Future_summary.pkl', 'rb')
# Fu20_dict = pickle.load(pkl_file)	;	pkl_file.close()  

# pkl_file = open('data/Nat-Hist_summary.pkl', 'rb')
# Hist_dict = pickle.load(pkl_file)	;	pkl_file.close()  

# lat=np.arange(-90,90,180/128.)
# lon=np.arange(0,358.59375,360/256.)


#########################	2-obs	####################################################
plt.clf()
fig,axes=plt.subplots(nrows=6,ncols=2,figsize=(10,12))
axes=axes.flatten()
count=0
for season in ['year','MAM','JJA','SON','DJF']:
	print season
	for state in [-1,1]:
		to_plot=Fu20_dict[season][state]['mean']-Hist_dict[season][state]['mean']
		to_plot[to_plot==0]=np.nan
		im1=plot_map.plot_map(to_plot,lat,lon,color_palette=plt.cm.PiYG_r,color_range=[-0.5,0.5],limits=[-180,180,-65,80],ax=axes[count],show=False,color_bar=False)
		if season=='year' and state==-1:	axes[count].set_title('cold persistence')
		if season=='year' and state==1:	axes[count].set_title('warm persistence')
		if state==-1:	axes[count].set_ylabel(season)
		count+=1

axes[count].axis('off')
axes[count+1].axis('off')

cbar_ax=fig.add_axes([0,0.1,1,0.15])
cbar_ax.axis('off')
cb=fig.colorbar(im1,orientation='horizontal',label='Difference in mean Period Length between +2$^{\circ} $C and Historical [days]')
fig.tight_layout()
plt.savefig('plots/diff_mean_Plus2-Hist.png',dpi=300)



#########################	hist validation	####################################################
pkl_file = open('../HadGHCND_persistence/data/HadGHCND_summary.pkl', 'rb')
obs_dict = pickle.load(pkl_file)	;	pkl_file.close()  

lat_obs=obs_dict['lat'][1:-1]
lon_obs=obs_dict['lon'][1:-1]

plt.clf()
fig,axes=plt.subplots(nrows=11,ncols=2,figsize=(10,22))
axes=axes.flatten()
count=0
for season in ['year','MAM','JJA','SON','DJF']:
	print season
	for state in [-1,1]:
		to_plot=Hist_dict[season][state]['mean']
		to_plot[to_plot==0]=np.nan
		im1=plot_map.plot_map(to_plot,lat,lon,color_palette=persis,color_range=[2,9],limits=[-180,180,-65,80],ax=axes[count],show=False,color_bar=False)
		if season=='year':	axes[count].set_title('MIROC Nat-Hist')
		if state==-1:	axes[count].set_ylabel(season+' cold')
		if state==1:	axes[count].set_ylabel(season+' warm')
		count+=1

		to_plot=obs_dict[season][state]['mean'][1:-1,1:-1]
		to_plot[to_plot==0]=np.nan
		im1=plot_map.plot_map(to_plot,lat_obs,lon_obs,color_palette=persis,color_range=[2,9],limits=[-180,180,-65,80],ax=axes[count],show=False,color_bar=False)
		if season=='year':	axes[count].set_title('HadGHCND')
		count+=1

axes[count].axis('off')
axes[count+1].axis('off')

cbar_ax=fig.add_axes([0.1,0.05,0.8,0.07])
cbar_ax.axis('off')
cb=fig.colorbar(im1,orientation='horizontal',label='Mean Period Length [days]')
fig.tight_layout()
plt.savefig('plots/Nat-Hist_HadGHCND_mean.png',dpi=300)










