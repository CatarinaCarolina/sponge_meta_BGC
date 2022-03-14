## Diversity visualization and statistical testing (figure 3)

Files needed:
Big-map: all_RPKMs_norm.tsv
sub_sponge_metadata_extra.xls

```
pyhton3 BGC_stats_ordination.py -i all_RPKMs_norm.tsv -m sub_sponge_metadata_extra.xls -o bgc_ordination.pdf -p bgc_permanova.txt -s bgc_shannon.pdf
```


```
pyhton3 taxa_ordination.py -i braycurtis_NTU.tsv -m sub_sponge_metadata_extra.xls -o taxa_ordination.pdf -p taxa_permanova.txt
```


```
pyhton3 diversity_tests.py -b shannon_bgc.tsv -t shannon_NTU.tsv -m sub_sponge_metadata_extra.xls -o pearson_corr.txt
```