import os
from spectra import Spectrum
import pandas as pd

def get_index_from_filename(filename):
	for i in range(4, len(filename)):
		if filename[i]!='0':
			return 'id'+filename[i:i+4]

PATH_NAME = 'spectra/'
files = os.listdir(PATH_NAME)
#if there is no csv file, create one and add column fields
if not os.path.exists('velocities-data.csv'): 
	f = open('velocities-data.csv', '+w')
	f.write('ID,STAR_V,STAR_V_ERR')
	f.close()

#sort filenames so that the results on csv file can appear in increasing order of the spectrum's id
files.sort()

#create results/ folder if it already doesn't exist
if not os.path.exists('results/'):
	os.mkdir('results/')

for f in files:
	index = get_index_from_filename(f)
	spec = Spectrum(PATH_NAME+f)
	print("Running MCMC on spectrum "+index)
	path_results = 'results/'+index+'/'
	if not os.path.exists(path_results):
		os.mkdir(path_results)
	#run mcmc method and save corner and walkers plot on path_results
	result = spec.fit_mcmc([4861.297761,6562.85175,8498.02,8542.09,8662.14],path_results)
	old_df = pd.read_csv('velocities-data.csv')
	data = {
		'ID': index,
		'STAR_V': result['avg_velocity'],
		'STAR_V_ERR': result['avg_uncertainty']
	}
	new_df = pd.DataFrame([data],columns=list(data.keys()))
	updated_df = pd.concat([old_df,new_df])
	updated_df.to_csv('velocities-data.csv',index=False)
print('Completed')