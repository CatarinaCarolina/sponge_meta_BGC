#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to take a pariwise distance matrix, compute orditation stats,
and plot a PcoA
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

bc_df = pd.read_csv(bc_matrix_path, sep='\t', index_col=0)
meta_df = pd.read_excel(meta_path, index_col=0)
sample_n = meta_df['True_sample']

BC_dist = skbio.stats.distance.DistanceMatrix(bc_df, ids=sample_n)

bc_perm = skbio.stats.distance.permanova(BC_dist, grouping=meta_df['Species extra'])

bc_perm_fobj = open(perm_path, 'w')
bc_perm_fobj.write(str(bc_perm))
bc_perm_fobj.close()

bc_pcoa = skbio.stats.ordination.pcoa(BC_dist)
#print(bc_pcoa.proportion_explained)

bc_pcoa_df =bc_pcoa.samples[['PC1','PC2']]

labels = meta_df['Species extra']

bc_pcoa_df.insert(2,'Label', labels)

sns.set_style("white")
sns.scatterplot(data=bc_pcoa_df, x='PC1', y='PC2', hue='Label', palette=["#ffc410","#8a4bc9","#8d9091","#525454","#32a1ab","#14cdde"], alpha=0.85, s=100)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# # add label to points on the plot
# ax = plt.gca()
# for row in bc_pcoa_df.itertuples():
#     #print(row[0], row[1], row[2])
#     ax.text(x=row[1]+.01, y=row[2], s=row[0], color='black', fontsize='xx-small')

#plt.show()
plt.savefig(pcoa_path, transparent=True, facecolor='None', format='pdf', edgecolor='None', pad_inches=0.5, bbox_inches='tight')
