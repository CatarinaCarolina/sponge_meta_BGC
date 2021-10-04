#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to fetch GCFs and compile the GCF set per bin cluster
"""

import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-b', '-bin', dest='bin', help='rep bin info file',\
		 required=True, metavar='<file>')

	parser.add_argument('-g', '-gcf', dest='gcf', help='gcf info file',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='output bin_rep oriented',\
		 required=True, metavar='<file>')

	return parser.parse_args()


def parse_gcf(gcf_file):
	"""
	A function to extract GCF,bin, class info

	gcf_file: str, filepath
	gcf_class_dict: dict{gcf:class}
	bin_gcf_dict: dict{bin:[gcf]}
	gcf_samples_dict: dict{gcf:[samples]}
	"""

	gcf_class_dict = {}
	bin_gcf_dict = {}
	gcf_samples_dict = {}

	file_obj = open(gcf_file, 'r')

	for line in file_obj:
		line = line.strip()
	
		bgc,contig,gclass,gcf,sample,bin = line.split('\t')
	
		gcf_class_dict[gcf] = gclass
	
		if bin not in bin_gcf_dict.keys():
			bin_gcf_dict[bin] = [gcf]
		else:
			bin_gcf_dict[bin].append(gcf)

		if gcf not in gcf_samples_dict.keys():
			gcf_samples_dict[gcf] = [sample]
		else:
			gcf_samples_dict[gcf].append(sample)
	file_obj.close()

	return (gcf_class_dict,bin_gcf_dict,gcf_samples_dict)

def update_bin_info(bin_rep_file, out_file, gcf_class_dict,bin_gcf_dict,gcf_samples_dict,dict_eco_groups):
	"""
	A function to update binrep info to include gcf info

	bin_rep_file: str, filepath
	out_file: str, filepath
	gcf_class_dict: dict{gcf:class}
	bin_gcf_dict: dict{bin:[gcf]}
	gcf_samples_dict: dict{gcf:[samples]}
	dict_eco_groups: dict{group:[samples]}
	"""

	header = '#cluster\tbinrep\tsamples\tbins\tecogroups\tGCFs\tGCF_class\tGCF_samples\tGCF_ecogroups\tGCF_allecogroups\n'

	b_fileobj = open(bin_rep_file, 'r')
	out_fileobj = open(out_file, 'w')

	out_fileobj.write(header)

	for line in b_fileobj:
		line = line.strip()
		bins = line.split('\t')[3].split(',')
		bin_rep = line.split('\t')[1]

		gcfs = []
		gcf_classes = []
		gcf_samples = []
		gcf_eco = []

		gcfs_in_bin_group = False

		for bin in bins:
			if bin not in bin_gcf_dict.keys():
				continue
			else:
				gcfs_in_bin_group = True
				for gcf in bin_gcf_dict[bin]:
					if gcf not in gcfs:
						eco_groups = []
						gcfs.append(gcf)
						gcf_classes.append(gcf_class_dict[gcf])
						gcf_samples.append(gcf_samples_dict[gcf])

						for sample in gcf_samples_dict[gcf]:
							for eco in dict_eco_groups.keys():
								if sample+'_' in dict_eco_groups[eco] and eco not in eco_groups:
									eco_groups.append(eco)
						gcf_eco.append(eco_groups)

		if gcfs_in_bin_group:
			w_gcfs = ','.join(gcfs)
			w_classes = ','.join(gcf_classes)
			w_samples = ','.join([str(sample_set) for sample_set in gcf_samples])
			w_teco = ','.join(set([inner for outer in gcf_eco for inner in outer]))
			w_eco = ','.join([str(eco_set) for eco_set in gcf_eco])
			
			out_fileobj.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(line,w_gcfs,w_classes,w_samples,w_eco,w_teco))

		else:
			out_fileobj.write('{}\t-\t-\t-\t-\t-\n'.format(line))

	b_fileobj.close()
	out_fileobj.close()

	return None

if __name__ == '__main__':

	cmds = get_cmds()

	ecogroup2_samples = {'Aplysina':['Aply16_', 'Aply21_', 'Aply22_', 'Aply23_'],\
			'Geodia_shallow':['gb2_2_', 'gb3_2_', 'gb4_2_', 'gb5_2_', 'gb6_'],\
			'Geodia_mid':['gb1_','gb7_', 'gb8_2_','gb9_','gb10_'],\
			'Geodia_deep':['gb126_', 'gb278_', 'gb305_'],\
			'Petrosia':['Pf4_', 'Pf5_', 'Pf6_','Pf7_', 'Pf8_', 'Pf9_','Pf10_', 'Pf11_', 'Pf12_'],\
			'Med_SW':['sw_7_', 'sw_8_', 'sw_9_'],\
			'Atl_SW': ['gb_1_f_', 'gb_2_f_', 'gb_f_3_','gb5_6_f_', 'gb_f_9_', 'gb10_f_']}


	bin_rep_f =  cmds.bin
	gcf_f = cmds.gcf
	out_f = cmds.out

	dict_gcf_class,dict_bin_gcf,dict_gcf_samples = parse_gcf(gcf_f)

	update_bin_info(bin_rep_f, out_f, dict_gcf_class,dict_bin_gcf,dict_gcf_samples, ecogroup2_samples)
