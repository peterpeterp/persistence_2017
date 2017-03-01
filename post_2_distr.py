import os,sys,glob,time,collections,gc,pickle
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date


#scenario='Nat-Hist'
#scenario='Plus15-Future'
#scenario='Plus20-Future'
seasons=['MAM','JJA','DJF','SON','year']

pkl_file = open('data/'+scenario+'_counter.pkl', 'rb')
distr_dict = pickle.load(pkl_file)	;	pkl_file.close()  

#nc_in=Dataset('data/tas_Aday_MIROC5_Plus15-Future_CMIP5-MMM-est1_v2-0_run001.nc','r')
nc_in=Dataset('data/raw/tas_Aday_MIROC5_Plus15-Future_CMIP5-MMM-est1_v2-0_run001.nc','r')
lat=nc_in.variables['lat'][:]
lon=nc_in.variables['lon'][:]
nc_in.close()

out_dict={}
for season in seasons:
	out_dict[season]={}
	for state in [-1,1]:
		out_dict[season][state]={}
		out_dict[season][state]=np.zeros([len(lat),len(lon),100,2])

for iy in range(len(lat)):
	for ix in range(len(lon)):
		grid_cell=distr_dict[str(lat[iy])+'_'+str(lon[ix])]
		grid_cell['year']=grid_cell['MAM']+grid_cell['JJA']+grid_cell['SON']+grid_cell['DJF']

for season in seasons:
	print season
	for iy in range(len(lat)):
		start=time.time()
		print iy
		for ix in range(len(lon)):
			counter=distr_dict[str(lat[iy])+'_'+str(lon[ix])][season]
			tmp_counter=np.array([counter.keys(),[counter[a] for a in counter.keys()]]).T

			for state in [-1,1]:
				out_dict[season][-1][iy,ix,:,0]=range(100)
				distr=tmp_counter[tmp_counter[:,0]*state>0]
				distr[:,0]*=state
				for length,occurence in zip(distr[:,0],distr[:,1]):
					if length>=100:		out_dict[season][state][iy,ix,99,1]=occurence
					else:				out_dict[season][state][iy,ix,length,1]=occurence


		print time.time()-start

out_dict['lon']=lon
out_dict['lat']=lat

output = open('data/'+scenario+'_distr.pkl', 'wb')
pickle.dump(out_dict, output)
output.close()


