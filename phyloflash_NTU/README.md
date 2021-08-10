## processing of phyloFlash NTU table

BrayCurtis dissimilarity is used in taxonomy stats_ordination, genus level

```
python3 phylo_ntu_braycurtis.py -n phyloFlash_compare.6.ntu_table.tsv -o braycurtis_NTU.tsv
```

Shannon diversity dotplot is used in Figure 2, phylum level

```
python3 phylo_ntu_shannon.py -n phyloFlash_compare.2.ntu_table.tsv -o shannon_dotplot.pdf
```