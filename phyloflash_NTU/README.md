## processing of phyloFlash NTU table

BrayCurtis dissimilarity is used in taxonomy stats_ordination

```
python3 phylo_ntu_braycurtis.py -n phyloflash_NTU.tsv -o braycurtis_NTU.tsv
```

Shannon diversity dotplot is used in Figure 2.

```
python3 phylo_ntu_shannon.py -n phyloflash_NTU.tsv -o shannon_dotplot.pdf
```