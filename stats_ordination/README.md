## Generation of PERMANOVA analysis and PcoA visualization at BGC and taxonomy level
 PcoAs generated correspond to figure 2
 Pearson's r and p-value calculation from shannon diversity values
 
```
pyhton3 BGC_stats_ordination.py -i BiG-MAP/all_RPKMs_norm.tsv -m total_sponge_metadata_extra_hma.xls -o bgc_ordination.pdf -p bgc_permanova.txt -s bgc_shannon.pdf
```


```
pyhton3 taxa_ordination.py -i braycurtis_NTU.tsv -m total_sponge_metadata_extra_hma.xls -o taxa_ordination.pdf -p taxa_permanova.txt
```


```
pyhton3 diversity_correlation.py -b shannon_bgc.tsv -t shannon_NTU.tsv -m total_sponge_metadata_extra_hma.xls -o pearson_corr.txt
```