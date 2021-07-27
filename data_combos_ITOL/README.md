# series description

## GCF oriented descriptive dataset building

###extract BGC, contig, class

```
cat bigscape/network_files/2020-11-20_17-44-52_hybrids_auto/Network_Annotations_Full.tsv | grep -v 'BGC0' | awk -F '\t' '{print $1"\t"$3"\t"$5}' > BGC_contig_class.tsv
```

### extract GCF, sample
```
python3 BGC_to_GFC.py -i BGC_contig_class.tsv -g bigscape/network_files/2020-11-20_17-44-52_hybrids_auto/mix/mix_clustering_c0.50.tsv -o BGC_contig_class_gcf_sample.tsv
```

### extract bin

```
python3 from_contig_get_bin.py -i BGC_contig_class_gcf_sample.tsv -o BGC_contig_class_gcf_sample_bin_ap.tsv -b all_refined_bins
```

## Dereplicated MAG oriented descriptive dataset building

### get list of all dereplicated representative MAGs

```
ls dereplicated_genomes/ > representative_genomes.txt
```

### make bin_cluster info table bin_cluster bins rep_bin samples

```
python3 compile_bin_cluster_info.py -r representative_genomes.txt -c dREP_out/data_tables/Cdb.csv -o cluster_rep_bins_samples_ap.tsv
```

### add GCFs/classes to bin_rep oriented table

```
python3 GCF_to_bin_rep.py -b cluster_rep_bins_samples_ap.tsv -g BGC_contig_class_gcf_sample_bin_ap.tsv -o cluster_rep_bins_samples_GCF_gsamples_ap.tsv
```

#datasets for ITOL

```
python3 make_binrep_classif.py -i gtdbtk.bac120.summary.tsv -o itol_db_bin_classification_ap.tsv
```

```
python3 make_binrep_sample_table.py -b cluster_rep_bins_samples_GCF_gsamples_ap.tsv -o itol_db_bin_ecosample_df_ap.tsv
```

```
python3 make_binrep_gcfclass.py -b cluster_rep_bins_samples_GCF_gsamples_ap.tsv -o itol_db_bin_gcf_class_ap.ts
```

ITOL dataset formats were further adjusted in excel to match input requirements