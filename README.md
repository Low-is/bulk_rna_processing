# bulk_rna_processing

## WSL and Ubuntu Installation
```
# WindowsPowerShell

wsl --install
wsl --install -d Ubuntu
```

## Run Ubuntu
```
# WindowsPowerShell
wsl -d Ubuntu

# Will ask to create user name and password...
# Press `ENTER` for username
# Create simple password, nothing will appear on the screen, no dots or asterisks. This is normal for Linux
```

## Install the tools needed to build STAR
```
# Ubuntu

sudo apt update
sudo apt install -y wget tar make g++

# May ask for Linux password
```


## Download STAR 2.7.11b
```
# Ubuntu

wget https://github.com/alexdobin/STAR/archive/2.7.11b.tar.gz
```

## Extract the STAR files
```
# Ubuntu

tar -xzf 2.7.11b.tar.gz
cd STAR-2.7.11b/source
```


## Move STAR into Linux home directory
```
# Ubuntu

cd ~
mv /mnt/c/Users/loisr/STAR-2.7.11b .
cd ~/STAR-2.7.11b/source
```


# Instal Zlib (if needed)
```
# Ubuntu
# If given this error, install zlib:
# fatal error: zlib.h: No such file or directory
# Will ask for Linux password

sudo apt install -y zlib1g-dev
```


# Compile STAR 
```
# Ubuntu

make STAR
```


## Install STAR (can be ran anywhere)
```
# Ubuntu

sudo cp STAR /usr/local/bin/
```


## Create reference directory
```
# Ubuntu

mkdir -p ~/genomes/h38
cd ~/genomes/h38
```


# Download Ensembl release 99 / GRCh38 (human reference genome)
```
# Ubuntu

wget https://ftp.ensembl.org/pub/release-99/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
```


## Download matching Ensembl release 99 GTF annotation 
```
# Ubuntu

wget https://ftp.ensembl.org/pub/release-99/gtf/homo_sapiens/Homo_sapiens.GRCh38.99.gtf.gz
```


# Unzip FASTA and GTF
```
# Ubuntu

gunzip Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
gunzip Homo_sapiens.GRCh38.99.gtf.gz
```


## Determined read length of trimmed FASTQ files
```
# Ubuntu

zcat /mnt/d/Projects/animal_projects/animal_brain/Lauren_Jantzie_RNASeq/LJO1JHU504_striatum/fastq/127791_5_R1.trimmed.fastq.gz | awk 'NR==2 {print length($0); exit}'

# If output: 150
# --sjdbOverhang 149

# If output: 100
# --sjdbOverhang 99
```


## Build STAR Index
```
# Ubuntu

mkdir -p ~/genomes/h38/STAR

STAR \
  --runThreadN 16 \
  --runMode genomeGenerate \
  --genomeDir ~/genomes/h38/STAR \
  --genomeFastaFiles ~/genomes/h38/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
  --sjdbGTFfile ~/genomes/h38/Homo_sapiens.GRCh38.99.gtf \
  --sjdbOverhang 149
```


## Need more RAM?
```
# Ubuntu

exit # will exit WSL-Ubuntu to PowerShell

# PowerShell
notepad "$env:USERPROFILE\.wslconfig"
# Notepad will ask if you want to create this file, click "Yes"

wsl --shutdown # restart WSL


# Ubuntu
wsl -d Ubuntu # start Ubuntu again
free -h # Verify new memory
```

## Clone Repository
```
# Bash  

git clone https://github.com/Low-is/bulk_rna_processing.git
cd bulk_rna_processing
```

## Create Python venv
```
# Bash

python -m venv venv
source venv/Scripts/activate # Git Bash command
```


## Run bulk RNA-seq processing
```
# Bash

python bulk_rna_processing.py
```
