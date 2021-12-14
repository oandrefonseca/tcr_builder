# TCR database and Utils scripts
**Do not run!** Documentation purposes only.

-----

## 1. VDJ database

- Download VDJ from Antigenomics Github on the **tcr_builder/data** folder

```
wget https://github.com/antigenomics/vdjdb-db/releases/download/2021-09-05/vdjdb-2021-09-05.zip
unzip vdjdb-2021-09-05.zip -d vdjdb
rm vdjdb-2021-09-05.zip

```

## 2. TCRModel database

- Go to https://tcrmodel.ibbr.umd.edu/index
- Save page as TCRmodel.html on the **tcr_builder/data** folder


## 3. IMGT-HLA database

- Download HLA proteins sequences on IMGT-HLA repository

```

wget https://github.com/ANHIG/IMGTHLA/raw/Latest/fasta/hla_prot.fasta -O IMGT_HLA.prot.fasta

```

To be sure which are HLA ids, please check it at: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5805642/

## 4. Prepare databases (Under construction)

- Install and running snakemake

```
pip install -y snakemake
snakemake
```