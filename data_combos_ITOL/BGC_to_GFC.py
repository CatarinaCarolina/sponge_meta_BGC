#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to match BGCs with their GCF number & sample
"""
import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-i', '-in_f', dest='in_f', help='working input file with BGCs',\
		 required=True, metavar='<file>')

	parser.add_argument('-g', '-gcf', dest='gcf', help='bgc to gcf file',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out_f', dest='out_f',help='input with added gcf and sample',\
		 required=True, metavar='<file>')

	return parser.parse_args()



def parse_gcf(gcf_file):
	"""
	A function to extract BGC to GCF link

	gcf_dict: dict{BGC:CGF}
	sample_dict: dict(BGC:sample)
	"""

	file_obj = open(gcf_file, 'r')

	gcf_dict = {}
	sample_dict = {}

	for line in file_obj:
		if line.startswith('#'):
			continue
		line = line.strip()
		BGC,GCF = line.split('\t')
		if BGC.startswith('BGC'):
			continue
		gcf_dict[BGC] = GCF
		sample = BGC.split('_c')[0]
		sample_dict[BGC] = sample

	file_obj.close()
	return (gcf_dict, sample_dict)

def parse_linked(in_file, gcf_dict, sample_dict, out_file):
	"""
	A function to add GCF and sample columns to tsv

	in_file: str, file path
	out_file: str, file path
	gcf_dict: dict{BGC:CGF}
	sample_dict: dict{BGC:sample}
	"""

	in_fobj = open(in_file, 'r')
	out_fobj = open(out_file, 'w')

	for line in in_fobj:
		line = line.strip()
		if line.startswith('#'):
			out_fobj.write('{}\tGCF\tBGC_sample\n'.format(line))

		else:
			iBGC,icontig,iclass = line.split('\t')
			if iclass.startswith('PKS'):
				iclass = 'PKS'
			GCF = gcf_dict[iBGC]
			sample = sample_dict[iBGC]

			out_fobj.write('{}\t{}\t{}\t{}\t{}\n'.format(iBGC,icontig,iclass,GCF,sample))

	
	in_fobj.close()
	out_fobj.close()

	return None


if __name__ == '__main__':

	cmds = get_cmds()

	input_tsv = cmds.in_f
	gcf_tsv = cmds.gcf
	output_tsv = cmds.out_f

	dict_gcf,dict_sample = parse_gcf(gcf_tsv)

	parse_linked(input_tsv, dict_gcf, dict_sample, output_tsv)
