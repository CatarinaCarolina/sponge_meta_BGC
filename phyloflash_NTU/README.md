## processing of phyloFlash NTU table for figure 3

BrayCurtis dissimilarity is used in taxonomy stats_ordination, genus level

```
python3 phylo_ntu_braycurtis.py -n phyloFlash_compare.6.ntu_table.hma.tsv -o braycurtis_NTU.tsv
```

Shannon diversity dotplot is used in Figure 3, genus level

```
python3 phylo_ntu_shannon.py -n phyloFlash_compare.6.ntu_table.hma.tsv -o shannon_dotplot.pdf
```