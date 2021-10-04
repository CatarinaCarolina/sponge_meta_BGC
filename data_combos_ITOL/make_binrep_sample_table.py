#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to make itol db of binrep to eco samples
"""

import argparse
import pandas as pd

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-b', '-bin', dest='bin', help='binrep info file',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='itol binrep sample db',\
		 required=True, metavar='<file>')

	return parser.parse_args()



def parse_binrep(binrep_file, out_file):
	"""
	A function to build itol db of binrep to ecosample

	binrep_file: str, filepath
	out_file: str, filepath
	"""

	bin_fobj = open(binrep_file, 'r')

	bin_eco = {}

	for line in bin_fobj:
		line = line.strip()
		if line.startswith('#'):
			header = line

		else:
			bin = line.split('\t')[1]
			bin = bin.replace('_', ' ').replace('.fa','')
			eco = line.split('\t')[4].split(',')

			bin_eco[bin] = {'Med_SW':0,'Atl_SW':0,'Aplysina':0,'Petrosia':0,'Geodia_shallow':0,'Geodia_mid':0,'Geodia_deep':0}
	
			for seco in eco:
				bin_eco[bin][seco] += 1

	bin_eco_df = pd.DataFrame.from_dict(bin_eco, orient='index')

	#print(bin_eco_df)

	bin_eco_df.to_csv(out_file, sep = '\t')

	bin_fobj.close()
	return None

if __name__ == '__main__':

	cmds = get_cmds()

	binrep_f = cmds.bin
	out_f = cmds.out

	parse_binrep(binrep_f, out_f)
