#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to create a binrep gcf table
"""

import argparse
import pandas as pd

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-b', '-bin', dest='bin', help='binrep file',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='bin gcf table',\
			 required=True, metavar='<file>')

	return parser.parse_args()


def parse_binrep(binrep_file, out_file):
	"""
	A function to make a gcf x bin table

	binrep_file: str, filepath 
	out_file: str, filepath
	"""

	bin_fobj = open(binrep_file, 'r')

	bin_gcf_dict = {}

	for line in bin_fobj:
		line = line.strip()
		if line.startswith("#"):
			header = line
		else:
			bin = line.split('\t')[1]
			bin = bin.replace('_',' ')
			classes = line.split('\t')[6].split(',')
			bin_gcf_dict[bin] = {'PKS':0,'NRPS':0,'RiPPs':0,'Terpene':0,'Others':0}

			for gcf in classes:
				if gcf in bin_gcf_dict[bin].keys():
					bin_gcf_dict[bin][gcf] += 1

	bin_gcf_df = pd.DataFrame.from_dict(bin_gcf_dict, orient='index')
	
	bin_gcf_df.to_csv(out_file, sep = '\t')

	return None

if __name__ == '__main__':

	cmds = get_cmds()

	binrep_f = cmds.bin
	out_f = cmds.out

	parse_binrep(binrep_f, out_f)
