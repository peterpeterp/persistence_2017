import os,sys,glob

working_path='/global/cscratch1/sd/pepflei/MIROC/'

scenario_list=[path.split('/')[-1] for path in glob.glob(working_path+'*')]

for scenario in scenario_list:
	all_files=glob.glob(working_path+scenario+'/*')
	for file in all_files:
		if 'land.nc' not in file.split('_'):
			os.system('cdo mul '+file+' /global/homes/p/pepflei/masks/landmask_128x256_NA-1.nc '+file.replace('.nc','_land.nc'))





