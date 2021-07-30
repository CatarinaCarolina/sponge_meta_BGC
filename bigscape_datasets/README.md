# Dataset generation from bigscape output

make_bigscape_matrices.py generates all matrices and intermediate dicts necessary for the downstream plotting scripts

```
python3 make_bigscape_matrices.py -l Network_Annotations_Full.tsv -n mix_c0.50.network -b mix_clustering_c0.50.tsv -o BGC_as5_full_mix_0.5_ -m total_sponge_metadata.csv
```

```
python3 barchart.py -b BGC_class_matrix.pickle -o barchart_figure.pdf -m total_sponge_metadata.csv 
```

```
python3 heatmap.py -l links_matrix.pickle -o heatmap_figure.pdf 
```

```
python3 upsetplot.py -d sample_mix_dict.pickle -o upsetplot_figure.pdf
```

```
python3 rarefaction_lines.py -d sample_GCF_dict.pickle -o rarefaction_lines_figure.pdf
```