import os,sys,glob,time,collections,gc,pickle
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date

seasons=['MAM','JJA','DJF','SON','year']

pkl_file = open('data/Plus20-Future_distr.pkl', 'rb')
Plus20 = pickle.load(pkl_file)	;	pkl_file.close()  

pkl_file = open('data/Nat-Hist_distr.pkl', 'rb')
Hist = pickle.load(pkl_file)	;	pkl_file.close() 

lon=Hist['lon']
lat=Hist['lat']

out_dict={}
for season in seasons:
	out_dict[season]={}
	for state in [-1,1]:
		out_dict[season][state]={}
		print season,state

		for iy in range(len(lat)):
			start=time.time()
			print iy
			for ix in range(len(lon)):
			counter=distr_dict[str(lat[iy])+'_'+str(lon[ix])][season]
			tmp=[]
			lengths=counter.keys()
			if 0 in lengths: 
				lengths.remove(0)
			if len(lengths)>2:
				for key in lengths:
					for i in range(counter[key]):
						tmp.append(key)
				tmp=np.array(tmp)
				tmp_dict={-1:tmp[tmp<0],1:tmp[tmp>0]}
				for state in [-1,1]:
					out_dict[season][state]['mean'][iy,ix]=np.mean(state*tmp_dict[state])
					for qu in [1,5,10,25,50,75,90,95,99]:
						out_dict[season][state][qu][iy,ix]=np.percentile(state*tmp_dict[state],qu)

		print time.time()-start

out_dict['lon']=lon
out_dict['lat']=lat

output = open('data/'+scenario+'_summary.pkl', 'wb')
pickle.dump(out_dict, output)
output.close()


