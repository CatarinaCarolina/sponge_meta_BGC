# Dataset generation from bigscape output

make_bigscape_matrices.py generates all matrices and intermediate dicts necessary for the downstream plotting scripts

```
python3 make_bigscape_matrices.py -l Network_Annotations_Full.hma.tsv -n mix_c0.50.hma.network -b mix_clustering_c0.50.hma.tsv -o BS_AS5_ -m total_sponge_metadata_hma.csv
```

figure 1a,1e
```
python3 barchart.py -b BS_AS5_BGC_class_matrix.pickle -o barchart_figure.pdf -m total_sponge_metadata_extra_hma.xls 
```

```
python3 heatmap.py -l BS_AS5_links_matrix.pickle -o heatmap_figure.pdf 
```

```
python3 rarefaction_lines.py -d BS_AS5_sample_GCF_dict.pickle -o rarefaction_lines_figure.pdf
```

figure 4
```
python3 upsetplot.py -d BS_AS5_sample_mix_dict.pickle -o upsetplot_figure.pdf
```