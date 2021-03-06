import os,sys,glob
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date

def temp_anomaly_to_ind(anom_file,out_file,var_name='tas',seasons={'MAM':[3,4,5],'JJA':[6,7,8],'SON':[9,10,11],'DJF':[12,1,2]},overwrite=True):

	nc_in=Dataset(anom_file,'r')
	time=nc_in.variables['time'][:]
	datevar = num2date(time,units = nc_in.variables['time'].units,calendar = nc_in.variables['time'].calendar)
	month=np.array([int(str(date).split("-")[1])	for date in datevar[:]])

	anom=nc_in.variables[var_name][:,:,:]


	for season in seasons.keys():
		days_in_seayson=np.where( (month==seasons[season][0]) | (month==seasons[season][1]) | (month==seasons[season][2]) )[0]
		seasonal_median=np.nanmedian(anom[days_in_seayson,:,:],axis=0)
		anom[days_in_seayson,:,:]-=seasonal_median

	anom[anom>=0] = 1
	anom[anom<0] = -1

	if overwrite: os.system('rm '+out_file)
	nc_out=Dataset(out_file,'w')
	for dname, the_dim in nc_in.dimensions.iteritems():	nc_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)
	for v_name, varin in nc_in.variables.iteritems():
		if v_name!=var_name:
			outVar = nc_out.createVariable(v_name, varin.datatype, varin.dimensions)
			outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
			outVar[:] = varin[:]
		else: 
			outVar = nc_out.createVariable('state','i1',('time','lat','lon',))
			outVar.description='daily anomalies - seasonal medain of daily anomalies at grid cell level. positive anomalies -> 1 negative anomalies -> -1'
			outVar[:] = anom

	nc_out.close()
	nc_in.close()


# test
# temp_anomaly_to_ind('tas_anom_Aday_MIROC5_Plus15-Future_CMIP5-MMM-est1_v2-0_run001.nc','tas_anom_Aday_MIROC5_Plus15-Future_CMIP5-MMM-est1_v2-0_run001_state.nc')

working_path='/global/cscratch1/sd/pepflei/MIROC/'

scenario_list=[path.split('/')[-1] for path in glob.glob(working_path+'*')]
for scenario in scenario_list:
	all_files=glob.glob(working_path+scenario+'/*_land_anom*')
	for file in all_files:
		if 'state.nc' not in file.split('_'):
			print file
			temp_anomaly_to_ind(file,file.replace('.nc','_state.nc'),overwrite=True)



