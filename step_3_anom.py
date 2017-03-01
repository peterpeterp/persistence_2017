import os,sys,glob

working_path='/global/cscratch1/sd/pepflei/MIROC/'

scenario_list=[path.split('/')[-1] for path in glob.glob(working_path+'*')]

for scenario in scenario_list:
	all_files=glob.glob(working_path+scenario+'/*_land*')
	for file in all_files:
		if 'anom.nc' not in file.split('_'):
			os.system('cdo -ydaysub '+file+' -ydaymean '+file+' '+file.replace('.nc','_anom.nc'))



