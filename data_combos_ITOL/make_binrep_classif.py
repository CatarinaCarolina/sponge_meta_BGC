#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to make a tsv of bin & classification
"""

import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-i', '-gtdb', dest='gtdb', help='gtdbtk classification summary',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='itol db formatted',\
		 required=True, metavar='<file>')

	return parser.parse_args()


def parse_gtdb(gtdb_sum_file, out_db_file):
	"""
	Function to parse and build bin classification databse

	gtdb_sum_file: str, filepath
	out_db_file: str, filepath
	"""

	gtdb_fobj = open(gtdb_sum_file, 'r')
	out_fobj = open(out_db_file, 'w')


	for line in gtdb_fobj:
		line = line.strip()

		if line.startswith('user'):
			header = line
		else:
			elms = line.split('\t')
			bin = elms[0]
			tax = elms[1]
			
			bin = bin.replace('_', ' ')
			tax = ','.join([tax.split(';')[1],tax.split(';')[5]])

			out_fobj.write('{}\t{}\n'.format(bin, tax))

	gtdb_fobj.close()
	out_fobj.close()

	return None


if __name__ == '__main__':

	cmds = get_cmds()

	gtdb_file = cmds.gtdb
	out_file = cmds.out

	parse_gtdb(gtdb_file,out_file )
