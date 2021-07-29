#!/bin/env python3

"""
Author: Catarina Loureiro

A script to take the bigscape GCF links matrix and generate a (log10) heatmap
"""
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='Plot GCF links\
        into a heatmap')

    parser.add_argument('-l', '--links', dest='links', help=\
        'GCF links matrix pickle', required=True, metavar='<file>')

    parser.add_argument('-o', '--out', dest='out', help=\
        'output figure file path', required=True, metavar='<file>')

    return parser.parse_args()


def cluster_map_vis(matrix_file,new_cols, outname, log=False):
    """
    A function to visualize df into a heatmap

    matrix_file: binary, pickle file
    new_cols: list[str], ordered samples
    outname: str, out file path
    log: toggle, apply log10
    """

    df = pd.read_pickle(matrix_file)
    new_df = df[new_cols]
    new_df = new_df.reindex(new_cols)

    cmap3 = sns.cubehelix_palette(500, start=2.8, rot=-0.3, dark=0.1, light=1, reverse=True,\
                                  gamma=0.8, hue=1)
    plt.figure(figsize=(13, 10))

    if log:
        log_df = np.log10(new_df).replace(-np.inf, 0)
        hm = sns.heatmap(log_df, fmt='d', xticklabels=True, yticklabels=True, cmap=cmap3)
    else:
        hm = sns.heatmap(new_df, fmt='d', xticklabels=True, yticklabels=True, cmap=cmap3)

    hm.set_xticklabels(hm.get_xmajorticklabels(), fontsize=14)
    hm.set_yticklabels(hm.get_ymajorticklabels(), fontsize=14)

    #	plt.show()
    plt.savefig(outname, transparent=True, facecolor='None', format='pdf', \
                edgecolor='None', pad_inches=0.5, bbox_inches='tight')

    return None

if __name__ == '__main__':

    cmds = get_cmds()

    sorted_samples = ['Aply16_', 'Aply21_', 'Aply22_', 'Aply23_', 'Cr15_', 'Cr50_', 'Cr90_', 'Dys1.1_',\
                      'Dys1.2_', 'Dys2.1_', 'Pf4_', 'Pf5_', 'Pf6_', 'Pf7_', 'Pf8_', 'Pf9_', 'Pf10_', 'Pf11_',\
                      'Pf12_', 'gb1_', 'gb2_2_', 'gb3_2_', 'gb4_2_', 'gb5_2_', 'gb6_', 'gb7_', 'gb8_2_', 'gb9_',\
                      'gb10_', 'gb126_', 'gb278_', 'gb305_', 'gb_1_f_', 'gb_2_f_', 'gb_f_3_', 'gb5_6_f_',\
                      'gb_f_9_', 'gb10_f_', 'sw_7_', 'sw_8_', 'sw_9_']

    cluster_map_vis(cmds.links, sorted_samples, cmds.out, log=True)