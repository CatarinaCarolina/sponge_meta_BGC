#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to take a pariwise distance matrix and compute orditation stats
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import skbio as skbio

def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '-matrix', dest='matrix', help='NTU braycurtis matrix', \
                        required=True, metavar='<file>')
    parser.add_argument('-m', '-meta', dest='meta', help='metadata table', \
                        required=True, metavar='<file>')
    parser.add_argument('-o', '-out_pcoa', dest='out_pcoa', help='ordination plot pcoa', \
                        required=True, metavar='<file>')
    parser.add_argument('-p', '-out_perm', dest='out_perm', help='permanova results', \
                        required=True, metavar='<file>')

    return parser.parse_args()

cmds = get_cmds()

meta_path = cmds.meta
bc_matrix_path = cmds.matrix
pcoa_path = cmds.out_pcoa
perm_path = cmds.out_perm


sample_n = ['Aply16', 'Aply21', 'Aply22', 'Aply23', 'Cr15', 'Cr50', 'Cr90', 'Dys1.1', 'Dys1.2', 'Dys2.1', 'Pf10', 'Pf11', 'Pf12', 'Pf4', 'Pf5', 'Pf6', 'Pf7', 'Pf8', 'Pf9','gb1', 'gb2_2', 'gb3_2', 'gb4_2', 'gb5_2', 'gb6', 'gb7', 'gb8_2', 'gb9', 'gb10','gb126', 'gb278', 'gb305', 'gb1_f', 'gb2_f', 'gb3_f', 'gb5_6_f', 'gb9_f', 'gb10_f', 'sw_7', 'sw_8', 'sw_9']


bc_df = pd.read_csv(bc_matrix_path, sep='\t', index_col=0)
meta_df = pd.read_excel(meta_path, index_col=0)

BC_dist = skbio.stats.distance.DistanceMatrix(bc_df, ids=sample_n)

bc_perm = skbio.stats.distance.permanova(BC_dist, grouping=meta_df['Species extra'])

bc_perm_fobj = open(perm_path, 'w')
bc_perm_fobj.write(str(bc_perm))
bc_perm_fobj.close()

bc_pcoa = skbio.stats.ordination.pcoa(BC_dist)
#print(bc_pcoa.proportion_explained)

bc_pcoa_df =bc_pcoa.samples[['PC1','PC2']]

colours = ["#ffc410","#ffc411","#ffc412","#ffc413","#dc2a3d","#dc2a3d","#dc2a3d","#eb4ad0","#eb4ad1","#eb4ad2","#8a4bc9","#8a4bc10","#8a4bc11","#8a4bc12","#8a4bc13","#8a4bc14","#8a4bc15","#8a4bc16","#8a4bc17","#cedbde","#cedbde",  "#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#b0bcbf","#b0bcbf","#b0bcbf","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#14cdde","#14cdde","#14cdde"]

labels = ["Aplysina aerophoba","Aplysina aerophoba","Aplysina aerophoba","Aplysina aerophoba","Crambe crambe","Crambe crambe","Crambe crambe","Dysidea avara","Dysidea avara","Dysidea avara","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Can","Geodia barretti Can","Geodia barretti Can","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Med","Seawater Med","Seawater Med"]

bc_pcoa_df.insert(2,'Label', labels)

sns.set_style("white")
sns.scatterplot(data=bc_pcoa_df, x='PC1', y='PC2', hue='Label', palette=["#ffc410", "#c70e22", "#e86dd3", "#8a4bc9","#8d9091","#525454","#32a1ab","#14cdde"], alpha=0.75)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# # add label to points on the plot
# ax = plt.gca()
# for row in bc_pcoa_df.itertuples():
#     #print(row[0], row[1], row[2])
#     ax.text(x=row[1]+.01, y=row[2], s=row[0], color='black', fontsize='xx-small')

#plt.show()
plt.savefig(pcoa_path, transparent=True, facecolor='None', format='pdf', edgecolor='None', pad_inches=0.5, bbox_inches='tight')
