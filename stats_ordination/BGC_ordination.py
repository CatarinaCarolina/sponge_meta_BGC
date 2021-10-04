#!usr/bin/python3

"""
Author: Catarina Loureiro
A script to take the Jaccard GCF matrix and compute ordination stats,
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

    parser.add_argument('-i', '-matrix', dest='matrix', help='BGC jaccard matrix', \
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
matrix_path = cmds.matrix
pcoa_path = cmds.out_pcoa
perm_path = cmds.out_perm

sample_n = ['Aply16_','Aply21_','Aply22_','Aply23_','Pf4_','Pf5_','Pf6_','Pf7_','Pf8_','Pf9_','Pf10_','Pf11_','Pf12_','gb1_','gb2_2_','gb3_2_','gb4_2_','gb5_2_','gb6_','gb7_','gb8_2_','gb9_','gb10_','gb126_','gb278_','gb305_','gb_1_f_','gb_2_f_','gb_f_3_','gb5_6_f_','gb_f_9_','gb10_f_','sw_7_','sw_8_','sw_9_']

meta_df = pd.read_excel(meta_path, index_col=14)
dist_df = pd.read_csv(matrix_path, sep='\t', index_col=0)

rev_df = 1 - dist_df

DM_bgc_links = skbio.stats.distance.DistanceMatrix(rev_df, ids=sample_n)

perm = skbio.stats.distance.permanova(DM_bgc_links, grouping=meta_df['Species extra'])

perm_fobj = open(perm_path, 'w')
perm_fobj.write(str(perm))
perm_fobj.close()

pcoa = skbio.stats.ordination.pcoa(distance_matrix=DM_bgc_links, method='eigh', number_of_dimensions=3, inplace=False)
print(pcoa.proportion_explained)

pcoa_df =pcoa.samples[['PC1','PC2']]

colours = ["#ffc410","#ffc411","#ffc412","#ffc413","#8a4bc9","#8a4bc10","#8a4bc11","#8a4bc12","#8a4bc13","#8a4bc14","#8a4bc15","#8a4bc16","#8a4bc17","#cedbde","#cedbde",  "#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#cedbde","#b0bcbf","#b0bcbf","#b0bcbf","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#32a1ab","#14cdde","#14cdde","#14cdde"]


labels = ["Aplysina aerophoba","Aplysina aerophoba","Aplysina aerophoba","Aplysina aerophoba","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Petrocia ficiformis","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Nor","Geodia barretti Can","Geodia barretti Can","Geodia barretti Can","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Atl","Seawater Med","Seawater Med","Seawater Med"]

pcoa_df.insert(2,'Label', labels)

sns.set_style("white")
sns.scatterplot(data=pcoa_df, x='PC1', y='PC2', hue='Label', palette=["#ffc410", "#8a4bc9","#8d9091","#525454","#32a1ab","#14cdde"], alpha=0.85, s=100)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# # for visible label points on the plot
# ax = plt.gca()
# for row in pcoa_df.itertuples():
#     #print(row[0], row[1], row[2])
#     ax.text(x=row[1]+.02, y=row[2], s=row[0], color='black', fontsize='xx-small')

#plt.show()
plt.savefig(pcoa_path, transparent=True, facecolor='None', format='pdf', edgecolor='None', pad_inches=0.5, bbox_inches='tight')