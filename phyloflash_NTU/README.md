## processing of phyloFlash NTU table

BrayCurtis dissimilarity is used in taxonomy stats_ordination, genus level

```
python3 phylo_ntu_braycurtis.py -n phyloflash_NTU_6.tsv -o braycurtis_NTU.tsv
```

Shannon diversity dotplot is used in Figure 2, phylum level

```
python3 phylo_ntu_shannon.py -n phyloflash_NTU_2.tsv -o shannon_dotplot.pdf
```