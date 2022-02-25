#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to take 2 sets of alpha diversity values and calculate a number of statistics
"""
import argparse
import pandas as pd
from scipy.stats import spearmanr
import numpy as np
from scipy.stats import kruskal

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
    parser.add_argument('-o', '-out', dest='out', help='div statistics output', \
                        required=True, metavar='<file>')

    return parser.parse_args()

cmds = get_cmds()

meta_path = cmds.meta
sbgc_path = cmds.bgc
staxa_path = cmds.taxa
out_path = cmds.out
file_out = open(out_path, 'w')

meta_df = pd.read_excel(meta_path, index_col=0)
sbgc_df = pd.read_csv(sbgc_path, sep= '\t', index_col=0)
staxa_df = pd.read_csv(staxa_path, sep= '\t', index_col=0)

all_pcorr, all_ppval = spearmanr(staxa_df['0'], sbgc_df['0'])
print('All Pearson',all_pcorr, all_ppval)
file_out.write(f"Pearson's r: {all_pcorr}\n")
file_out.write(f'p value: {all_ppval}\n')

sponge_samples = meta_df.loc[meta_df['Type'] == 'Sponge Tissue'].index
geodiacan_samples = meta_df.loc[meta_df['Species extra'] == 'Geodia barretti Can'].index
geodianor_samples = meta_df.loc[meta_df['Species extra'] == 'Geodia barretti Nor'].index
petrosia_samples = meta_df.loc[meta_df['Species'] == 'Petrocia ficiformis'].index
aplysina_samples = meta_df.loc[meta_df['Species'] == 'Aplysina aerophoba'].index
water_samples = meta_df.loc[meta_df['Type'] == 'Filtered Sea Water'].index

sponge_sbgc_df = sbgc_df.loc[sponge_samples]
sponge_staxa_df = staxa_df.loc[sponge_samples]
geodiacan_sbgc_df = sbgc_df.loc[geodiacan_samples]
geodiacan_staxa_df = staxa_df.loc[geodiacan_samples]
geodianor_sbgc_df = sbgc_df.loc[geodianor_samples]
geodianor_staxa_df = staxa_df.loc[geodianor_samples]
petrosia_sbgc_df = sbgc_df.loc[petrosia_samples]
petrosia_staxa_df = staxa_df.loc[petrosia_samples]
aplysina_sbgc_df = sbgc_df.loc[aplysina_samples]
aplysina_staxa_df = staxa_df.loc[aplysina_samples]
water_sbgc_df = sbgc_df.loc[water_samples]
water_staxa_df = staxa_df.loc[water_samples]



file_out.write(f"Sponge Mean BGC: {np.mean(sponge_sbgc_df['0'])}\n")
file_out.write(f"Sponge STD BGC: {np.std(sponge_sbgc_df['0'])}\n")
file_out.write(f"Sponge VAR BGC: {np.var(sponge_sbgc_df['0'])}\n")

file_out.write(f"Sponge Mean Taxa: {np.mean(sponge_staxa_df['0'])}\n")
file_out.write(f"Sponge STD Taxa: {np.std(sponge_staxa_df['0'])}\n")
file_out.write(f"Sponge VAR Taxa: {np.var(sponge_staxa_df['0'])}\n")

file_out.write(f"geodianor Mean BGC: {np.mean(geodianor_sbgc_df['0'])}\n")
file_out.write(f"geodianor STD BGC: {np.std(geodianor_sbgc_df['0'])}\n")
file_out.write(f"geodianor VAR BGC: {np.var(geodianor_sbgc_df['0'])}\n")

file_out.write(f"geodianor Mean Taxa: {np.mean(geodianor_staxa_df['0'])}\n")
file_out.write(f"geodianor STD Taxa: {np.std(geodianor_staxa_df['0'])}\n")
file_out.write(f"geodianor VAR Taxa: {np.var(geodianor_staxa_df['0'])}\n")

file_out.write(f"geodiacan Mean BGC: {np.mean(geodiacan_sbgc_df['0'])}\n")
file_out.write(f"geodiacan STD BGC: {np.std(geodiacan_sbgc_df['0'])}\n")
file_out.write(f"geodiacan VAR BGC: {np.var(geodiacan_sbgc_df['0'])}\n")

file_out.write(f"geodiacan Mean Taxa: {np.mean(geodiacan_staxa_df['0'])}\n")
file_out.write(f"geodiacan STD Taxa: {np.std(geodiacan_staxa_df['0'])}\n")
file_out.write(f"geodiacan VAR Taxa: {np.var(geodiacan_staxa_df['0'])}\n")

file_out.write(f"petrosia Mean BGC: {np.mean(petrosia_sbgc_df['0'])}\n")
file_out.write(f"petrosia STD BGC: {np.std(petrosia_sbgc_df['0'])}\n")
file_out.write(f"petrosia VAR BGC: {np.var(sponge_sbgc_df['0'])}\n")

file_out.write(f"petrosia Mean Taxa: {np.mean(petrosia_staxa_df['0'])}\n")
file_out.write(f"petrosia STD Taxa: {np.std(petrosia_staxa_df['0'])}\n")
file_out.write(f"petrosia VAR Taxa: {np.var(petrosia_staxa_df['0'])}\n")

file_out.write(f"aplysina Mean BGC: {np.mean(aplysina_sbgc_df['0'])}\n")
file_out.write(f"aplysina STD BGC: {np.std(aplysina_sbgc_df['0'])}\n")
file_out.write(f"aplysina VAR BGC: {np.var(aplysina_sbgc_df['0'])}\n")

file_out.write(f"aplysina Mean Taxa: {np.mean(aplysina_staxa_df['0'])}\n")
file_out.write(f"aplysina STD Taxa: {np.std(aplysina_staxa_df['0'])}\n")
file_out.write(f"aplysina VAR Taxa: {np.var(aplysina_staxa_df['0'])}\n")

file_out.write(f"Water Mean BGC: {np.mean(water_sbgc_df['0'])}\n")
file_out.write(f"Water STD BGC: {np.std(water_sbgc_df['0'])}\n")
file_out.write(f"Water VAR BGC: {np.var(water_sbgc_df['0'])}\n")
file_out.write(f"Water Mean Taxa: {np.mean(water_staxa_df['0'])}\n")
file_out.write(f"Water STD Taxa: {np.std(water_staxa_df['0'])}\n")
file_out.write(f"Water VAR Taxa: {np.var(water_staxa_df['0'])}\n")


kruskal_res = kruskal(geodiacan_sbgc_df, geodianor_sbgc_df, petrosia_sbgc_df, aplysina_sbgc_df)
file_out.write(f"kruskal all: {kruskal_res}\n")
kruskal_res_gb = kruskal(geodiacan_sbgc_df, geodianor_sbgc_df)
file_out.write(f"kruskal gbs: {kruskal_res_gb}\n")
kruskal_res_gb_aa = kruskal(geodianor_sbgc_df, aplysina_sbgc_df)
file_out.write(f"kruskal gb aa: {kruskal_res_gb_aa}\n")
kruskal_res_aa_pf = kruskal(petrosia_sbgc_df, aplysina_sbgc_df)
file_out.write(f"kruskal pf aa: {kruskal_res_aa_pf}\n")
kruskal_res_gb_pf = kruskal(geodianor_sbgc_df, petrosia_sbgc_df)
file_out.write(f"kruskal gb pf: {kruskal_res_gb_pf}\n")

kruskal_taxares = kruskal(geodiacan_staxa_df, geodianor_staxa_df, petrosia_staxa_df, aplysina_staxa_df)
file_out.write(f"kruskal taxa all: {kruskal_taxares}\n")
kruskal_taxares_gb = kruskal(geodiacan_staxa_df, geodianor_staxa_df)
file_out.write(f"kruskal taxa gbs: {kruskal_taxares_gb}\n")
kruskal_taxares_gb_aa = kruskal(geodianor_staxa_df, aplysina_staxa_df)
file_out.write(f"kruskal taxa gb aa: {kruskal_taxares_gb_aa}\n")
kruskal_taxares_aa_pf = kruskal(petrosia_staxa_df, aplysina_staxa_df)
file_out.write(f"kruskal taxa pf aa: {kruskal_taxares_aa_pf}\n")
kruskal_taxares_gb_pf = kruskal(geodianor_staxa_df, petrosia_staxa_df)
file_out.write(f"kruskal taxa gb pf: {kruskal_taxares_gb_pf}\n")


file_out.close()

