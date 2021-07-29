#!/bin/env python3

"""
Author: Catarina Loureiro

A script to take the bigscape GCF presence/absence and generate upsetplot figure
"""

import argparse
import matplotlib.pyplot as plt
import upsetplot
import pickle


def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='Plot GCF sample\
            intersect in an UpsetPlot')

    parser.add_argument('-d', '--dict_mix', dest='dict_mix', help=\
        'sample_mix_dict pickle file', required=True, metavar='<file>')

    parser.add_argument('-o', '--out', dest='out', help=\
        'output figure file path', required=True, metavar='<file>')

    return parser.parse_args()


def GCF_transform_eco(big_sample_pickle, sample_grouping_dict):
    """
    A function to transfer GCF:samples to GCF:eco groups

    big_sample_dict:dict{GCF_nr:[samples]}
    sample_grouping_dict: dict{group:[samples]}
    big_eco_dict:dict{GCF_nr:[sample_groups]}
    """

    f_obj = open(big_sample_pickle, 'rb')
    big_sample_dict = pickle.load(f_obj)

    big_eco_dict = {GCF: [] for GCF in big_sample_dict.keys()}

    for GCF, sample_list in big_sample_dict.items():
        for sample in sample_list:
            for ecogroup, samples in sample_grouping_dict.items():
                if sample in samples and ecogroup not in big_eco_dict[GCF]:
                    big_eco_dict[GCF].append(ecogroup)

    return big_eco_dict


def pyupset_data(big_sps_dict, species_list, outname):
    """
    A function to transform data into pyupset format

    species_list:[str] sps names
    big_sps_dict: dict{GCF:[samples]}
    sample_setname: str,idd for figure printing
    sps_pyupset_dict: dict{sample_combo:value}
    """

    sps_pyupset_dict = {sps: [] for sps in species_list}

    for GCF, groups in big_sps_dict.items():
        for sps in groups:
            if GCF not in sps_pyupset_dict[sps]:
                sps_pyupset_dict[sps].append(GCF)

    content_data = upsetplot.from_contents(sps_pyupset_dict)

    fig = upsetplot.UpSet(content_data, sort_by='degree', sort_categories_by='cardinality', subset_size='auto', \
                          show_counts='%d', facecolor='#2F6C7E')
    fig.plot()
    # plt.show()
    plt.savefig(outname, transparent=True, facecolor='None', \
                orientation='landscape', format='pdf', edgecolor='None')
    plt.close()

    return sps_pyupset_dict

if __name__ == '__main__':

    cmds = get_cmds()

    semigroup_samples = {'Aplysina': ['Aply16_', 'Aply21_', 'Aply22_', 'Aply23_'], \
                         'Crambe': ['Cr15_', 'Cr50_', 'Cr90_'], \
                         'Dysidea': ['Dys1.1_', 'Dys1.2_', 'Dys2.1_'], \
                         'Geodia_NOR': ['gb1_', 'gb2_2_', 'gb3_2_', 'gb4_2_', 'gb5_2_', 'gb6_', 'gb7_', 'gb8_2_', \
                                        'gb9_', 'gb10_'], \
                         'Geodia_CAN': ['gb126_', 'gb278_', 'gb305_'], \
                         'Petrosia': ['Pf4_', 'Pf5_', 'Pf6_', 'Pf7_', 'Pf8_', 'Pf9_', 'Pf10_', 'Pf11_', 'Pf12_'], \
                         'Med_SW': ['sw_7_', 'sw_8_', 'sw_9_'], \
                         'Atl_SW': ['gb_1_f_', 'gb_2_f_', 'gb_f_3_', 'gb5_6_f_', 'gb_f_9_', 'gb10_f_']}

    semigroup_list = ['Aplysina', 'Crambe', 'Dysidea', 'Geodia_NOR', 'Geodia_CAN', 'Petrosia', 'Med_SW', \
                      'Atl_SW']

    semi_sample_dict = GCF_transform_eco(cmds.mix_dict, semigroup_samples)

    pyupset_data(semi_sample_dict, semigroup_list, cmds.out)