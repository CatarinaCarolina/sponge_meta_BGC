#!/bin/env python3

"""
Author: Catarina Loureiro

A script to take the bigscape GCF class info and produce barchart figure
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
sns.set_style('white')


def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='Plot GCF class info\
	    and assembly size in barchart')

    parser.add_argument('-b', '--bcg_class', dest='bgc_class', help=\
        'BGC class count pickle', required=True, metavar='<file>')

    parser.add_argument('-o', '--out', dest='out', help=\
        'output figure file path', required=True, metavar='<file>')

    parser.add_argument('-m', '--metadata', dest='metadata', help=\
        'metadata xls', required=True, metavar='<file>')

    return parser.parse_args()



def cluster_class_vis(df_pickle, meta_path, out_file):
    """
    A function to plot a bar chart with BGC classes

    class_df_pickle: pickle object pandas.df
    new_cols: list[str], sorted sample order
    """

    meta_df = pd.read_excel(meta_path, index_col=14)
    new_cols = meta_df['True_sample']
    assembly_df = meta_df[['Assembly size (>4000bp)']]

    df = pd.read_pickle(df_pickle)
    new_df = df.reindex(new_cols)

    colour4 = ['#000000']
    cmap3 = sns.cubehelix_palette(5, start=2.8, rot=-0.3, dark=0.3, light=0.9, reverse=False, gamma=0.8, hue=1)
    cmap3 = ListedColormap(cmap3.as_hex())
    cmap4 = sns.color_palette(colour4)

    fig, ax1 = plt.subplots(figsize=(15, 10))
    ax2 = ax1.twinx()
    bp = new_df.plot.bar(ax=ax1, stacked=True, width=1.0, colormap=cmap3)
    sp = sns.scatterplot(data=(assembly_df / 10 ** 6), ax=ax2, palette=cmap4, s=60)

    ax2.set_ylim(bottom=0, top=None)
    ax1.set_xticklabels(ax1.get_xmajorticklabels(), fontsize=14)
    ax1.tick_params(axis='y', which='both', labelsize=14)
    ax2.tick_params(axis='y', which='both', labelsize=14)
    ax1.set_ylabel('BGC counts', fontsize=14)
    ax2.set_ylabel('Assembly size Mbp (>4000 bp)', fontsize=14)
    ax1.legend(loc=(0.01, 0.80), fontsize=14)
    ax2.legend(loc='best', fontsize=14)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)

    #	plt.show()

    plt.savefig(out_file, transparent=True, facecolor='None', format='pdf',\
                edgecolor='None', pad_inches=0.5, bbox_inches='tight')
    plt.close()

    return None

if __name__ == '__main__':

    cmds = get_cmds()

    pickle_BGC_class = cmds.bgc_class
    sample_metadf = cmds.metadata
    fig_path = cmds.out

    class_bar = cluster_class_vis(pickle_BGC_class, sample_metadf, fig_path)