#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to take 2 sets of alpha diversity values and calculate a correlation coeficient
"""
import argparse
import pandas as pd
from scipy.stats import pearsonr


def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-t', '-taxa', dest='taxa', help='all_RPKM_NORM shannon', \
                        required=True, metavar='<file>')
    parser.add_argument('-b', '-bgc', dest='bgc', help='all_RPKM_NORM shannon', \
                        required=True, metavar='<file>')
    parser.add_argument('-m', '-meta', dest='meta', help='metadata table', \
                        required=True, metavar='<file>')
    parser.add_argument('-o', '-out', dest='out', help='correlation output', \
                        required=True, metavar='<file>')

    return parser.parse_args()

cmds = get_cmds()

meta_path = cmds.meta
sbgc_path = cmds.bgc
staxa_path = cmds.taxa
out_path = cmds.out

meta_df = pd.read_excel(meta_path, index_col=0)
sbgc_df = pd.read_csv(sbgc_path, sep= '\t', index_col=0)
staxa_df = pd.read_csv(staxa_path, sep= '\t', index_col=0)

all_pcorr, all_ppval = pearsonr(staxa_df['0'], sbgc_df['0'])
print('All Pearson',all_pcorr, all_ppval)

file_out = open(out_path, 'w')
file_out.write(f"Pearson's r: {all_pcorr}\n")
file_out.write(f'p value: {all_ppval}\n')
file_out.close()

