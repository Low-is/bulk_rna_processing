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


## Install STAR so it can be run from anywhere
```
# Ubuntu

sudo cp STAR /usr/local/bin/
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
