#!/bin/env python3

"""
Author: Catarina Loureiro

A script to take the bigscape GCF counts per sample and compute rarefaction curves
"""

import itertools
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
sns.set_style('white')

def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='Plot GCF sample\
            intersect in an UpsetPlot')

    parser.add_argument('-d', '--dict_GCF', dest='dict_GCF', help=\
        'sample_GCF_dict pickle file', required=True, metavar='<file>')

    parser.add_argument('-o', '--out', dest='out', help=\
        'output figure file path', required=True, metavar='<file>')

    return parser.parse_args()


def GCF_rarefaction_series(GCF_count_pickle, sample_group_dict):
    """
    A function to create a rarefaction series, i.e count new GCFs with each new sample

    GCF_count_dict: dict{sample:[GCFs]}
    sample_group_dict: dict{sample_group:[samples]}
    avg_series_dict: dict{sample_group:[[int]]}
    """

    f_obj = open(GCF_count_pickle, 'rb')
    GCF_count_dict = pickle.load(f_obj)

    avg_series_dict = {key: [] for key in sample_group_dict.keys()}

    for group, samples in sample_group_dict.items():
        i_comb = itertools.permutations(samples)
        combo_series = []
        for c, combo in enumerate(i_comb):
            curr_series = []
            curr_set = set()
            for i in range(len(combo)):
                c_sample = combo[i]
                curr_set.update(GCF_count_dict[c_sample])
                curr_series.append(len(curr_set))
            combo_series[c] = curr_series
        # average all combo series
        combo_arr = np.array(combo_series)
        combo_avg = np.mean(combo_arr, axis=0)
        combo_avg = np.rint(combo_avg)
        avg_series_dict[group] = list(combo_avg)

    return avg_series_dict

def plot_GCF_rar(avg_series_dict, file_out):
    """
	A function to plot rarefaction lines

	avg_series_dict: dict{sample_group:[[int]]}
	"""

    lp = sns.lineplot(data=avg_series_dict, dashes=False)
    lp.set(xlabel='Sample count', ylabel='GCF count')
    plt.savefig(file_out, transparent=True, facecolor='None', format='pdf',\
                edgecolor='None', pad_inches=0.5, bbox_inches='tight')

    return None

if __name__ == '__main__':

    cmds = get_cmds()

    semigroup_samples = {'Aplysina': ['Aply16_', 'Aply21_', 'Aply22_', 'Aply23_'], \
                         'Crambe': ['Cr15_', 'Cr50_', 'Cr90_'], \
                         'Dysidea': ['Dys1.1_', 'Dys1.2_', 'Dys2.1_'], \
                         'Geodia_S_M': ['gb1_', 'gb2_2_', 'gb3_2_', 'gb4_2_', 'gb5_2_', 'gb6_', 'gb7_', 'gb8_2_', \
                                        'gb9_', 'gb10_'], \
                         'Geodia_D': ['gb126_', 'gb278_', 'gb305_'], \
                         'Petrosia': ['Pf4_', 'Pf5_', 'Pf6_', 'Pf7_', 'Pf8_', 'Pf9_', 'Pf10_', 'Pf11_', 'Pf12_'], \
                         'Med_SW': ['sw_7_', 'sw_8_', 'sw_9_'], \
                         'Atl_SW': ['gb_1_f_', 'gb_2_f_', 'gb_f_3_', 'gb5_6_f_', 'gb_f_9_', 'gb10_f_']}


    rar_series = GCF_rarefaction_series(cmds.dict_GCF, semigroup_samples)

    plot_GCF_rar(rar_series, cmds.out)