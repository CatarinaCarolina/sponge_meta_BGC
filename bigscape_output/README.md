# Dataset generation from bigscape output

make_bigscape_matrices.py generates all matrices and intermediate dicts necessary for the downstream plotting scripts

Necessary files:
general: sub_total_sponge_metadata.csv/xls
bigscape: Network_Annotations_Full.tsv, mix_c0.50.network, mix_clustering_c0.50.tsv

```
python3 make_bigscape_matrices.py -l Network_Annotations_Full.tsv -n mix_c0.50.network -b mix_clustering_c0.50.tsv -o BS_AS5_ -m sub_total_sponge_metadata.csv
```

figure 1a,1b,1e
```
python3 barchart.py -b BS_AS5_BGC_class_matrix.pickle -o barchart_figure.pdf -m sub_total_sponge_metadata.xls
```

```
python3 heatmap.py -l BS_AS5_links_matrix.pickle -o heatmap_figure.pdf 
```

```
python3 rarefaction_lines.py -d BS_AS5_sample_GCF_dict.pickle -o rarefaction_lines_figure.pdf
```

Upsetplot (figure 2)
```
python3 upsetplot.py -d BS_AS5_sample_mix_dict.pickle -o upsetplot_figure.pdf
```