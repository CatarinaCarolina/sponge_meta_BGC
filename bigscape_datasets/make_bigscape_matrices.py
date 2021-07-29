#!/bin/env python3

"""
Author: Catarina Loureiro

A script to take the bigscape mix_clusterinf file and generate matrices
"""

import collections
from collections import defaultdict
from collections import OrderedDict
import os
import itertools
import argparse
import pandas as pd
import numpy as np
import random
import sklearn
import sklearn.metrics
import matplotlib.pyplot as plt
import seaborn as sns
import pyupset as pyu
import upsetplot
import math
sns.set_style('white')
from matplotlib.colors import ListedColormap

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='Transform a\
		 Bigscape mix_clusterinf matrix into a sample link\
		 matrix')

	parser.add_argument('-b', '--big_mix', dest='big_mix', help=\
		'mix_clustering tsv file', required=True, metavar='<file>')

	parser.add_argument('-n', '--net_mix', dest='net_mix', help=\
		'mix network file', required=True, metavar='<file>')

	parser.add_argument('-o', '--out', dest='out', help=\
		'output matrix tsv file', required=True, metavar='<file>')

	parser.add_argument('-l', '--list_bgc', dest='list_bgc', help=\
		'bgc list used in network', required=True, metavar='<file>')

	parser.add_argument('-m', '--metadata', dest='metadata', help=\
		'metadata csv file', required=True, metavar='<file>')

	return parser.parse_args()

def get_samples(cluster_list):
	"""
	A function to extract sample names

	cluster_list: str, txt file
	sample_names: list[str]
	"""
	file_obj = open(cluster_list, 'r')

	sample_names = []

	for line in file_obj:
		line = line.strip().split()
		cluster = line[0]
		if cluster.startswith('BGC'):
			continue
		sample = cluster.split('c')[0]
		if sample not in sample_names:
			sample_names.append(sample)

	return sample_names

def parse_metadata(meta_file, sample_names):
	"""
	A function to parse metadata file into dict

	meta_file: str, txt csv file
	meta_dict: dict{sample:[str]}
	"""

	meta_dict = {name: [] for name in sample_names}
	file_obj = open(meta_file, 'r')

	for line in file_obj:
		if 'Type' in line:
			header = line
			continue
		else:
			line = line.strip().split(';')
			sample = line[0]
			meta_dict[sample] = line[1:]

	meta_df = pd.read_csv(meta_file, sep=';', index_col=0)

	return (meta_df)

def outputting_df(df, out_prefix, matrix_name):
	"""
	A function to output dataframes

	df: pd.DataFrame
	out_prefix: str
	matrix name: str
	path_out: str, tsv file
	"""
	path_out = os.path.join(os.getcwd(), out_prefix + matrix_name + '.tsv')
	file_obj = open(path_out, 'w')
	df.to_csv(file_obj, sep='\t')
	file_obj.close()

	pickle_out = os.path.join(os.getcwd(), out_prefix + matrix_name + '.pickle')
	df.to_pickle(pickle_out)

	return path_out

def class_counts(cluster_list, sample_names):
	"""
	A function to get cluster class counts per sample

	cluster_list: str, txt file
	sample_names: list[str]
	sample_BGC_class: dict{sample:{class:count}}
	class_list: list[str]
	"""

	sample_BGC_class = {name:defaultdict(int) for name in sample_names}
	class_list = []
	file_obj = open(cluster_list, 'r')

	for line in file_obj:
		if line.startswith('BGC'):
			continue
		words = line.strip().split()
		cluster = words[0]
		c_sample = cluster.split('c')[0]
		BS_class = words[4]
		if BS_class.startswith('PKS'):
			BS_class = 'PKS'
		if BS_class.startswith('Saccharide'):
			BS_class = 'Others'
		if BS_class not in class_list:
			class_list.append(BS_class)
		for name in sample_names:
			if name == c_sample: #in cluster:
				sample_BGC_class[name][BS_class] += 1

	return (sample_BGC_class, class_list)

def BGC_class_df(sample_BGC_class, class_list, sample_names):
	"""
	A function to transform class counts per sample into a matrix

	sample_BGC_class: dict{sample:defaultdict(class:int)}
	class_list: list[str]
	sample_names: list[str]
	"""

	empty_df = pd.DataFrame(index=sample_names, columns=class_list)
	class_df = empty_df.fillna(0)

	for sample, classes in sample_BGC_class.items():
		for BGC in classes:
			class_df.loc[sample,BGC] = sample_BGC_class[sample][BGC]

	return class_df


if __name__ == '__main__':

	cmds = get_cmds()

	# get list of all samples
	sample_list = get_samples(cmds.list_bgc)

	#process metadata file
	sample_metadf = parse_metadata(cmds.metadata, sample_list)
	#save metadf as pickle/tsv
	outputting_df(sample_metadf, cmds.out, 'sample_meta_matrix')


	# generate matrix of BGC class counts per sample
	sample_BGC_class_dict, BGC_class_list = class_counts(cmds.list_bgc, sample_list)
	BGC_class_matrix = BGC_class_df(sample_BGC_class_dict, BGC_class_list, sample_list)
	# save BGC_class_matrix as pickle/tsv
	outputting_df(BGC_class_matrix, cmds.out, 'BGC_class_matrix')