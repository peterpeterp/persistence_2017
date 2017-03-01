import os,sys,glob,time,collections,gc,pickle
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date


import os,sys,glob,time,collections,gc,pickle
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date


working_path='/global/cscratch1/sd/pepflei/MIROC/'

seasons={'MAM':{'months':[3,4,5],'index':0}, 'JJA':{'months':[6,7,8],'index':1}, 'SON':{'months':[9,10,11],'index':2}, 'DJF':{'months':[12,1,2],'index':3}}

scenario_list=[path.split('/')[-1] for path in glob.glob(working_path+'*')]
for scenario in ['Nat-Hist']:
	all_files=glob.glob(working_path+scenario+'/*period*')

	nc_in=Dataset(all_files[0],'r')
	lat=nc_in.variables['lat'][:]
	lon=nc_in.variables['lon'][:]
	nc_in.close()

	distr_dict={}
	for y in lat:
		for x in lon:
			distr_dict[str(y)+'_'+str(x)]={'MAM':collections.Counter(),'JJA':collections.Counter(),'SON':collections.Counter(),'DJF':collections.Counter()}

	for file in all_files:
		start_time=time.time()
		print file
		nc_in=Dataset(file,'r')
		try:
			period_length=nc_in.variables['period_length'][:,:,:]
			period_season=nc_in.variables['period_season'][:,:,:]

			for iy in range(len(lat)):
				sys.stdout.write('.')	;	sys.stdout.flush()
				for ix in range(len(lon)):
					for season in seasons.keys():
						in_season=np.where(period_season[:,iy,ix]==seasons[season]['index'])[0]
						distr_dict[str(lat[iy])+'_'+str(lon[ix])][season]+=collections.Counter(period_length[:,iy,ix][in_season])
		except:
			failed_files=open(working_path+scenario+'/damaged_files.txt','w')
			failed_files.write(file+'\n')
			failed_files.close()

		print time.time()-start_time


	output = open('data/'+scenario+'_counter.pkl', 'wb')
	pickle.dump(distr_dict, output)
	output.close()



# pkl_file = open('Nat-Hist_summary.pkl', 'rb')
# out_dict = pickle.load(pkl_file)	;	pkl_file.close()  



















