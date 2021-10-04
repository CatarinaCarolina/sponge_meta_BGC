## Generation of PERMANOVA analysis and PcoA visualization at BGC and taxonomy level
 PcoAs generated correspond to figure 2
 
```
pyhton3 BGC_ordination.py -i BS_AS5_links_jaccard_matrix.tsv -m total_sponge_metadata_extra_hma.xls -o bgc_ordination.pdf -p bgc_permanova.txt
```


```
pyhton3 taxa_ordination.py -i braycurtis_NTU.tsv -m total_sponge_metadata_extra_hma.xls -o taxa_ordination.pdf -p taxa_permanova.txt
```