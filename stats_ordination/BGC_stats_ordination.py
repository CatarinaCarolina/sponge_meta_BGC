#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to turn the RPKM_NORM matrix from bigmap into pcoa ordination
"""
import argparse
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sns
import skbio as skbio

def get_cmds():
    """
    Capture args from the cmdline
    """

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '-matrix', dest='matrix', help='all_RPKM_NORM matrix', \
                        required=True, metavar='<file>')
    parser.add_argument('-m', '-meta', dest='meta', help='metadata table', \
                        required=True, metavar='<file>')
    parser.add_argument('-o', '-out_pcoa', dest='out_pcoa', help='ordination plot pcoa', \
                        required=True, metavar='<file>')
    parser.add_argument('-p', '-out_perm', dest='out_perm', help='permanova results', \
                        required=True, metavar='<file>')
    parser.add_argument('-s', '-out_shannon', dest='out_shannon', help='plot file\
    		shannon diversity', required=True, metavar='<file>')
    parser.add_argument('-b', '-out_braycurtis', dest='out_braycurtis', help='plot file\
    		shannon diversity', required=True, metavar='<file>')

    return parser.parse_args()

cmds = get_cmds()

meta_path = cmds.meta
all_RPKM_NORM_path = cmds.matrix
pcoa_path = cmds.out_pcoa
perm_path = cmds.out_per
shannon_path = cmds.out_shannon
bc_path = cmds.out_braycurtis


meta_df = pd.read_excel(meta_path)
sample_n_hmaex = meta_df['Name']
sample_n_hma = meta_df['Red_sample']

all_RPKM_NORM_df = pd.read_csv(all_RPKM_NORM_path, sep= '\t', index_col=0)
all_RPKM_NORM_df = all_RPKM_NORM_df[sample_n_hma]

bc_matrix = [[0] * len(sample_n_hma) for i in range(len(sample_n_hma))]

for col_1 in all_RPKM_NORM_df:
    vals_1 = all_RPKM_NORM_df[col_1]
    index_1 = all_RPKM_NORM_df.columns.get_loc(col_1)
    for col_2 in all_RPKM_NORM_df:
        vals_2 = all_RPKM_NORM_df[col_2]
        index_2 = all_RPKM_NORM_df.columns.get_loc(col_2)
        bc_val = distance.braycurtis(vals_1, vals_2)
        bc_matrix[index_1][index_2] = bc_val

bc_df = pd.DataFrame(bc_matrix, columns=sample_n_hmaex, index=sample_n_hmaex)
bc_df.to_csv(bc_path, sep='\t')

bc_dist_hma = skbio.stats.distance.DistanceMatrix(bc_df, ids=sample_n_hmaex)
bc_perm_hma = skbio.stats.distance.permanova(bc_dist_hma, grouping=meta_df['Species extra'])

bc_perm_fobj = open(perm_path, 'w')
bc_perm_fobj.write(str(bc_perm_hma))
bc_perm_fobj.close()

bc_pcoa_hma = skbio.stats.ordination.pcoa(bc_dist_hma)
print(bc_pcoa_hma.proportion_explained)

#bc_pcoa_porp_fobj = open(, 'w')
#bc_pcoa_porp_fobj.write(str(bc_pcoa_hma.proportion_explained))
#bc_pcoa_porp_fobj.close()

bc_pcoa_hma_df =bc_pcoa_hma.samples[['PC1','PC2']]
bc_pcoa_hma_df.insert(2,'Label', list(meta_df['Species extra']))

sns.set_style("white")
sns.scatterplot(data=bc_pcoa_hma_df, x='PC1', y='PC2', hue='Label', palette=["#ffc410","#8a4bc9","#8d9091","#525454","#32a1ab","#14cdde"], alpha=0.85, s=100)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# ax = plt.gca()
# # label points on the plo
# #for row in bc_pcoa_df.itertuples():
#     #print(row[0], row[1], row[2])
#     #ax.text(x=row[1]+.01, y=row[2], s=row[0], color='black', fontsize='xx-small')
#
#plt.show()
plt.savefig(pcoa_path, transparent=True, facecolor='None', format='pdf', edgecolor='None', pad_inches=0.5, bbox_inches='tight')
#
shannon_dict = {sample: 0 for sample in sample_n_hmaex}
for col in all_RPKM_NORM_df:
    ind = all_RPKM_NORM_df.columns.get_loc(col)
    vals = all_RPKM_NORM_df[col]
    shannon_score = skbio.diversity.alpha.shannon(vals)
    sample = sample_n_hmaex[ind]
    shannon_dict[sample] = shannon_score

sns.scatterplot(data=shannon_dict)
plt.xticks(rotation='vertical')
#plt.show()
plt.savefig(shannon_path)