# script series description for generation of figure 3

## GCF oriented descriptive dataset building

### extract BGC, contig, class

```
cat Network_Annotations_Full.hma.tsv | grep -v 'BGC0' | awk -F '\t' '{print $1"\t"$3"\t"$5}' > BGC_contig_class.tsv
```

### extract GCF, sample
```
python3 BGC_to_GFC.py -i BGC_contig_class.tsv -g mix_clustering_c0.50.hma.tsv -o BGC_contig_class_gcf_sample.tsv
```

### extract bin

```
python3 from_contig_get_bin.py -i BGC_contig_class_gcf_sample.tsv -o BGC_contig_class_gcf_sample_bin.tsv -b all_refined_bins/
```

## Dereplicated MAG oriented descriptive dataset building

### make bin_cluster info table bin_cluster bins rep_bin samples

```
python3 compile_bin_cluster_info.py -r representative_genomes.txt -c Cdb.csv -o cluster_rep_bins_samples.tsv
```

### add GCFs/classes to bin_rep oriented table

```
python3 GCF_to_bin_rep.py -b cluster_rep_bins_samples.tsv -g BGC_contig_class_gcf_sample_bin.tsv -o cluster_rep_bins_samples_GCF_gsamples.tsv
```

# datasets for ITOL

```
python3 make_binrep_classif.py -i gtdbtk.bac120.summary.tsv -o itol_db_bin_classification.tsv
```

```
python3 make_binrep_sample_table.py -b cluster_rep_bins_samples_GCF_gsamples.tsv -o itol_db_bin_ecosample_df.tsv
```

```
python3 make_binrep_gcfclass.py -b cluster_rep_bins_samples_GCF_gsamples.tsv -o itol_db_bin_gcf_class.ts
```

ITOL dataset formats were further adjusted in excel to match input requirements