import os,sys,glob

in_path='/project/projectdirs/m1517/C20C/MIROC/MIROC5/'
out_path='/global/cscratch1/sd/pepflei/MIROC/'

scenario_list=[path.split('/')[-1] for path in glob.glob(in_path+'*')]

for scenario in scenario_list:
	if scenario in ['All-Hist','Nat-Hist']:
		tmp_path=in_path+scenario+'/*/*/day/atmos/tas/'
		run_list=[path.split('/')[-1] for path in glob.glob(tmp_path+'*')]
		for run in run_list:
			out_file_name=glob.glob(tmp_path+run+'/*')[0].split('/')[-1].split(run)[0]+run+'.nc'
			os.system('rm '+out_path+scenario+'/'+out_file_name)
			command='cdo mergetime '+tmp_path+run+'/* '+out_path+scenario+'/'+out_file_name
			os.system(command)




cdo mul ifile land-sea-mask.nc ofile

# scp pepflei@cori.nersc.gov:/global/cscratch1/sd/pepflei/MIROC/Plus15-Future/*run001.nc data/raw/