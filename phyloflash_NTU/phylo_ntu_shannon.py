#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to parse the phyloflash compare ntu table and calculate a shannon diversity index
"""

import argparse
import skbio
import matplotlib.pyplot as plt
import seaborn as sns

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='parse phyloflash ntu table')

	parser.add_argument('-n', '-ntu', dest='ntu', help='tsv file\
		phyloflash ntu table', required=True, metavar='<file>')

	parser.add_argument('-p', '-plot', dest='plot', help='plot file\
			shannon diversity', required=True, metavar='<file>')

	return parser.parse_args()


def parse_file(ntu_file):
	"""
	A function to capture content of file column in lists

	nut_file: str, tsv file
	"""

	file_obj = open(ntu_file, 'r')

	taxa = []
	taxa_uniq = []
	samples = []
	counts = []

	for line in file_obj:
		line = line.strip()
		elm = line.split('\t')
		taxa.append(elm[0])
		if elm[0] not in taxa_uniq:
			taxa_uniq.append(elm[0])
		samples.append(elm[1])
		counts.append(elm[2])
	

	return (taxa, taxa_uniq, samples, counts)

def build_ntu_ltable(taxa,taxa_uniq,samples,samples_ord,counts):
	"""
	A function to build a matrix of counts

	empties: list[lists]: samples x taxa_uniq
	taxa:list[]
	taxa_uniq:list[]
	samples:list[]
	sample_ord:list[]
	counts:list[]
	"""

	empties = [[0]*len(taxa_uniq) for i in range(len(samples_ord))]

	for i in range(len(taxa)):
		taxon = taxa[i]
		samp = samples[i]
		count = counts[i]
		t_ind = taxa_uniq.index(taxon)
		s_ind = samples_ord.index(samp)

		empties[s_ind][t_ind] = int(count)

	return empties

def compute_shannon(empties, samples_nm):
	"""
	A function to compute shannon score per sample

	empties: list[lists]: samples[taxa_uniq]
	samples_nm:list[]
	shannon_dict: {str:int}, sample:score
	"""

	shannon_dict = {sample:0 for sample in samples_nm}
	
	for i in range(len(empties)):
		shannon_score = skbio.diversity.alpha.shannon(empties[i])
		sample = samples_nm[i]
		shannon_dict[sample] = shannon_score

	return shannon_dict

def plot_shannon(shannon_dict, plot_file):
	"""
	A function to plot scores in dotplot

	shannon_dict: {str:int}, sample:score
	outfile: str, filepath
	"""
	sns.scatterplot(data=shannon_dict)
	plt.xticks(rotation='vertical')
	plt.savefig(plot_file)

	return None

if __name__ == '__main__':

	cmds = get_cmds()

	l_taxa,l_taxa_u,l_samples,l_counts = parse_file(cmds.ntu)

	sample_names = ['Aply16_def_6', 'Aply21_def_6', 'Aply22_def_6', 'Aply23_def_6', 'Cr15_def_6', 'Cr50_def_6', 'Cr90_def_6', 'Dys1_1_def_6', 'Dys1_2_def_6', 'Dys2_1_def_6', 'Pf10_def_6', 'Pf11_def_6', 'Pf12_def_6', 'Pf4_def_6', 'Pf5_def_6', 'Pf6_def_6', 'Pf7_def_6', 'Pf8_def_6', 'Pf9_def_6','gb1_def_6', 'gb2_2_def_6', 'gb3_2_def_6', 'gb4_2_def_6', 'gb5_2_def_6', 'gb6_def_6', 'gb7_def_6', 'gb8_2_def_6', 'gb9_def_6', 'gb10_def_6','gb126_def_6', 'gb278_def_6', 'gb305_def_6', 'gb1_f_def_6', 'gb2_f_def_6', 'gb3_f_def_6', 'gb5_6_f_def_6', 'gb9_f_def_6', 'gb10_f_def_6', 'sw_7def_6', 'sw_8def_6', 'sw_9def_6']
	sample_n = ['Aply16', 'Aply21', 'Aply22', 'Aply23', 'Cr15', 'Cr50', 'Cr90', 'Dys1.1', 'Dys1.2', 'Dys2.1', 'Pf10', 'Pf11', 'Pf12', 'Pf4', 'Pf5', 'Pf6', 'Pf7', 'Pf8', 'Pf9','gb1', 'gb2_2', 'gb3_2', 'gb4_2', 'gb5_2', 'gb6', 'gb7', 'gb8_2', 'gb9', 'gb10','gb126', 'gb278', 'gb305', 'gb1_f', 'gb2_f', 'gb3_f', 'gb5_6_f', 'gb9_f', 'gb10_f', 'sw_7', 'sw_8', 'sw_9']

	ntu_ltable = build_ntu_ltable(l_taxa,l_taxa_u,l_samples,sample_names,l_counts)

	dict_shannon = compute_shannon(ntu_ltable, sample_n)

	plot_shannon(dict_shannon, cmds.plot)
